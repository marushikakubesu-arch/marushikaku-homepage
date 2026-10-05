# -*- coding: utf-8 -*-
"""納品書の品目を「まるしかくベース事業計画.xlsx」の台帳・資材シートに追加する。

使い方（Python 3.12）:
  python add_delivery.py 納品書.json            確認のみ（ファイルは書き換えない）
  python add_delivery.py 納品書.json --apply    台帳に書き込む
  python add_delivery.py --genus                台帳にある属と品種の一覧を出す
  --book パス                                   台帳ファイルの場所を指定（省略時はUSB等から自動で探す）
  --force                                       納品書の合計と合わなくても書き込む（確認済みのときだけ）

納品書.json の形（品名は属名を除いた品種名）:
{
  "仕入れ先": "GREEN MONSTERS",
  "納品書番号": "SOL-2",
  "仕入れ日": "2026-09-14",
  "納品書合計": 66000,
  "税込表記": false,
  "品目": [
    {"属": "ステファニア", "品名": "スベローサ", "区分": "植物", "単価": 1500, "個数": 2},
    {"品名": "60*10", "区分": "段ボール", "単価": 800, "個数": 1}
  ]
}
区分は 植物 / 用土 / 段ボール / ポット / 送料 / その他 のどれか（植物以外は資材シートへ）。
店頭価格を入れた品目は、その値を使う（人が決めた価格を優先）。
取引先の住所・電話番号などは入れない（台帳に入れるのは仕入れ先名だけ）。
"""
import argparse
import json
import math
import os
import re
import shutil
import sys
import unicodedata
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# ---------- 計算ルール（納品書自動計算/CLAUDE.md と同じ） ----------
TAX_RATE = Decimal("0.10")   # 消費税率
MARKUP = Decimal("2.5")      # 店頭販売価格の掛け率（たたき台）
ROUND_UNIT = 100             # 店頭販売価格の端数処理（切り捨て単位・円）

BOOK_NAME = "まるしかくベース事業計画.xlsx"
BOOK_DIR = "まるしかくベース"
SUPPLY_CATS = ("用土", "段ボール", "ポット", "送料", "その他")
ROUTES = ["店頭", "ヤフオク", "BASE", "Instagram", "店頭(プレゼント)"]


def find_book(arg):
    if arg:
        return arg
    env = os.environ.get("LEDGER_BOOK")
    if env:
        return env
    for letter in "DEFGHIJKLMNOPQRSTUVWXYZC":
        p = f"{letter}:\\{BOOK_DIR}\\{BOOK_NAME}"
        if os.path.exists(p):
            return p
    sys.exit(f"台帳ファイル（{BOOK_NAME}）が見つかりません。USBを挿してください。")


# ---------- 並び順（50音順） ----------
def kana_key(s):
    s = "".join(chr(ord(ch) + 0x60) if "ぁ" <= ch <= "ん" else ch for ch in s)
    d = unicodedata.normalize("NFD", s).replace("ー", "")
    return ("".join(ch for ch in d if ch not in "゙゚"), d)


def norm(s):
    return str(s).replace("　", " ").strip()


def base_variety(name):
    """末尾の個体番号を除いた品種名"""
    m = re.match(r"^(.*?)\s*(\d+)(?:\s+(.*))?$", name)
    if m and m.group(1):
        return (m.group(1).strip() + (" " + m.group(3).strip() if m.group(3) else "")).strip()
    return name


# ---------- 台帳の読み込み ----------
def to_date(v):
    if isinstance(v, datetime):
        return v.date()
    return v if isinstance(v, date) else None


def read_ledger(wb):
    items, supplies = [], []
    ws = wb["台帳"]
    genus = None
    for r in range(5, ws.max_row + 1):
        kind = ws.cell(r, 1).value
        if kind == "属":
            genus = ws.cell(r, 2).value
        elif kind == "個体":
            g = lambda c: ws.cell(r, c).value
            items.append(dict(genus=genus, variety=norm(g(2)), no=g(3), month=g(4), date=to_date(g(5)),
                              note=g(6), cost=g(7), lst=g(8), route=g(10), sold=g(11),
                              sdate=to_date(g(12)), fee=g(13)))
    ws = wb["資材"]
    for r in range(4, ws.max_row + 1):
        if ws.cell(r, 1).value and ws.cell(r, 2).value:
            supplies.append(dict(month=ws.cell(r, 1).value, cat=ws.cell(r, 2).value,
                                 name=ws.cell(r, 3).value, cost=ws.cell(r, 4).value))
    return items, supplies


# ---------- 台帳・資材・集計の書き出し ----------
FN = "Meiryo"
f_norm = Font(name=FN, size=10)
f_light = Font(name=FN, size=10, bold=False)
f_bold = Font(name=FN, size=11, bold=True)
f_head = Font(name=FN, size=10, bold=True, color="FFFFFF")
f_title = Font(name=FN, size=14, bold=True)
f_gray = Font(name=FN, size=8, color="999999")
fill_head = PatternFill("solid", fgColor="F28C28")
fill_genus = PatternFill("solid", fgColor="FDE9D2")
fill_in = PatternFill("solid", fgColor="FFFBE0")
thin = Side(style="thin", color="DDDDDD")
box = Border(top=thin, bottom=thin, left=thin, right=thin)
YEN = '#,##0;[Red]-#,##0;"-"'
DATE = "yyyy/mm/dd"


def write_sheets(wb, items, supplies):
    for n in ("台帳", "資材", "集計"):
        if n in wb.sheetnames:
            del wb[n]
    items = sorted(items, key=lambda i: (kana_key(i["genus"]), kana_key(i["variety"]), i["no"] or 0, i["month"]))
    genera = []
    for i in items:
        if i["genus"] not in genera:
            genera.append(i["genus"])

    # ----- 台帳 -----
    L = wb.create_sheet("台帳")
    L["A1"] = "植物の収支管理一覧（属名の50音順）"
    L["A1"].font = f_title
    heads = ["行", "属名／品種名", "個体No", "仕入れ月", "仕入れ日", "備考・仕入れ先", "仕入れ価格", "店頭販売価格",
             "状態", "販売ルート", "実販売価格", "販売日", "手数料・送料", "粗利"]
    HR = 4
    for j, h in enumerate(heads, 1):
        c = L.cell(HR, j, h)
        c.font, c.fill = f_head, fill_head
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for j, w in enumerate([5, 30, 8, 12, 12, 24, 12, 12, 10, 14, 12, 12, 12, 12], 1):
        L.column_dimensions[get_column_letter(j)].width = w
    row = HR + 1
    first = row
    for g in genera:
        gi = [i for i in items if i["genus"] == g]
        grow = row
        row += 1
        start = row
        for it in gi:
            L.cell(row, 1, "個体")
            L.cell(row, 2, "　" + it["variety"])
            L.cell(row, 3, it["no"])
            L.cell(row, 4, it["month"])
            L.cell(row, 5, it["date"]).number_format = DATE
            L.cell(row, 6, it["note"])
            L.cell(row, 7, it["cost"]).number_format = YEN
            L.cell(row, 8, it["lst"]).number_format = YEN
            L.cell(row, 9, f'=IF(K{row}<>"","販売済",IF(J{row}<>"","出品中","在庫"))')
            L.cell(row, 10, it["route"])
            L.cell(row, 11, it["sold"]).number_format = YEN
            L.cell(row, 12, it.get("sdate")).number_format = DATE
            L.cell(row, 13, it.get("fee")).number_format = YEN
            L.cell(row, 14, f'=IF(I{row}="販売済",K{row}-G{row}-M{row},"")').number_format = YEN
            for j in range(1, 15):
                c = L.cell(row, j)
                c.border = box
                c.font = f_gray if j == 1 else f_light
            for j in (12, 13):
                L.cell(row, j).fill = fill_in
            row += 1
        end = row - 1
        L.cell(grow, 1, "属")
        L.cell(grow, 2, g)
        L.cell(grow, 3, f"=COUNTA(B{start}:B{end})")
        L.cell(grow, 7, f"=SUM(G{start}:G{end})")
        L.cell(grow, 8, f"=SUM(H{start}:H{end})")
        L.cell(grow, 9, f'=COUNTIF(I{start}:I{end},"販売済")&"/"&COUNTA(B{start}:B{end})')
        L.cell(grow, 11, f"=SUM(K{start}:K{end})")
        L.cell(grow, 14, f"=SUM(N{start}:N{end})")
        for j in range(1, 15):
            c = L.cell(grow, j)
            c.fill, c.border = fill_genus, box
            c.font = f_gray if j == 1 else f_bold
            if j in (7, 8, 11, 14):
                c.number_format = YEN
            elif j in (3, 9):
                c.alignment = Alignment(horizontal="center")
    last = max(row - 1, first)
    rng = lambda col: f"${col}${first}:${col}${last}"
    L["A2"] = "合計（個体のみ）"
    L["A2"].font = f_bold
    for col in "GHKN":
        L[f"{col}2"] = f'=SUMIFS({rng(col)},{rng("A")},"個体")'
        L[f"{col}2"].number_format = YEN
        L[f"{col}2"].font = f_bold
    L["I2"] = f'=COUNTIFS({rng("A")},"個体",{rng("I")},"販売済")&"/"&COUNTIF({rng("A")},"個体")'
    L["I2"].font = f_bold
    L["A3"] = "黄色の列（販売日・手数料／送料）は、売れたときに入力します。状態は、実販売価格を入れると「販売済」、販売ルートだけ入れると「出品中」になります。"
    L["A3"].font = f_norm
    L.freeze_panes = L.cell(HR + 1, 3)
    L.auto_filter.ref = f"A{HR}:N{last}"
    # 販売ルートは選択式（一覧にない値は、確認のうえ入力もできる）
    dv = DataValidation(type="list", formula1='"' + ",".join(ROUTES) + '"', allow_blank=True,
                        errorStyle="warning", showErrorMessage=True, errorTitle="販売ルート",
                        error="一覧にない販売ルートです。このまま入力しますか？",
                        showInputMessage=True, promptTitle="販売ルート", prompt="▼から選んでください")
    dv.add(f"J{first}:J2000")
    L.add_data_validation(dv)

    # ----- 資材 -----
    S = wb.create_sheet("資材")
    S["A1"] = "資材（用土・段ボール・ポット・送料など）の仕入れ"
    S["A1"].font = f_title
    for j, h in enumerate(["仕入れ月", "区分", "品名", "金額"], 1):
        c = S.cell(3, j, h)
        c.font, c.fill = f_head, fill_head
    r = 4
    for s_ in supplies:
        for j, v in enumerate([s_["month"], s_["cat"], s_["name"], s_["cost"]], 1):
            c = S.cell(r, j, v)
            c.font, c.border = f_norm, box
        S.cell(r, 4).number_format = YEN
        r += 1
    s_last = max(r - 1, 4)
    for col, w in zip("ABCD", (12, 10, 24, 12)):
        S.column_dimensions[col].width = w

    # ----- 集計 -----
    T = wb.create_sheet("集計")
    T["A1"] = "集計"
    T["A1"].font = f_title
    LA = f"台帳!$A${first}:$A${last}"
    LC = lambda col: f"台帳!${col}${first}:${col}${last}"
    SA = lambda col: f"資材!${col}$4:${col}${s_last}"
    T["A3"] = "① 仕入れ月別"
    T["A3"].font = f_bold
    h1 = ["仕入れ月", "植物の仕入れ", "資材の仕入れ", "仕入れ合計", "植物の点数", "店頭販売価格の合計", "実販売額",
          "販売済", "出品中", "在庫", "粗利（販売済のみ）"]
    for j, h in enumerate(h1, 1):
        c = T.cell(4, j, h)
        c.font, c.fill = f_head, fill_head
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    mons = sorted({i["month"] for i in items} | {s_["month"] for s_ in supplies})
    for k, m in enumerate(mons):
        r = 5 + k
        T.cell(r, 1, m)
        T.cell(r, 2, f'=SUMIFS({LC("G")},{LA},"個体",{LC("D")},$A{r})')
        T.cell(r, 3, f'=SUMIFS({SA("D")},{SA("A")},$A{r})')
        T.cell(r, 4, f"=B{r}+C{r}")
        T.cell(r, 5, f'=COUNTIFS({LA},"個体",{LC("D")},$A{r})')
        T.cell(r, 6, f'=SUMIFS({LC("H")},{LA},"個体",{LC("D")},$A{r})')
        T.cell(r, 7, f'=SUMIFS({LC("K")},{LA},"個体",{LC("D")},$A{r})')
        for j, st in ((8, "販売済"), (9, "出品中"), (10, "在庫")):
            T.cell(r, j, f'=COUNTIFS({LA},"個体",{LC("D")},$A{r},{LC("I")},"{st}")')
        T.cell(r, 11, f'=SUMIFS({LC("N")},{LA},"個体",{LC("D")},$A{r})')
    rt = 5 + len(mons)
    T.cell(rt, 1, "合計")
    for j in range(2, 12):
        cl = get_column_letter(j)
        T.cell(rt, j, f"=SUM({cl}5:{cl}{rt-1})")
    for r in range(5, rt + 1):
        for j in range(1, 12):
            c = T.cell(r, j)
            c.font, c.border = (f_bold if r == rt else f_norm), box
            if j in (2, 3, 4, 6, 7, 11):
                c.number_format = YEN
    T.cell(rt + 1, 1, "注：「販売済」の点数と実販売額は、台帳に入力のある分だけです。").font = f_norm

    r0 = rt + 4
    T.cell(r0 - 1, 1, "② 販売ルート別").font = f_bold
    for j, h in enumerate(["販売ルート", "点数", "実販売額", "仕入れ価格", "粗利"], 1):
        c = T.cell(r0, j, h)
        c.font, c.fill = f_head, fill_head
    for k, rte in enumerate(ROUTES):
        r = r0 + 1 + k
        T.cell(r, 1, rte)
        T.cell(r, 2, f'=COUNTIFS({LA},"個体",{LC("J")},$A{r},{LC("I")},"販売済")')
        T.cell(r, 3, f'=SUMIFS({LC("K")},{LA},"個体",{LC("J")},$A{r})')
        T.cell(r, 4, f'=SUMIFS({LC("G")},{LA},"個体",{LC("J")},$A{r},{LC("I")},"販売済")')
        T.cell(r, 5, f'=SUMIFS({LC("N")},{LA},"個体",{LC("J")},$A{r})')
    rt2 = r0 + 1 + len(ROUTES)
    T.cell(rt2, 1, "合計")
    for j in range(2, 6):
        cl = get_column_letter(j)
        T.cell(rt2, j, f"=SUM({cl}{r0+1}:{cl}{rt2-1})")
    for r in range(r0 + 1, rt2 + 1):
        for j in range(1, 6):
            c = T.cell(r, j)
            c.font, c.border = (f_bold if r == rt2 else f_norm), box
            if j >= 3:
                c.number_format = YEN
    T.cell(rt2 + 1, 1, "注：ヤフオクの実販売価格は落札価格です。").font = f_norm

    r1 = rt2 + 4
    T.cell(r1 - 1, 1, "③ 売れ残り（在庫・出品中）").font = f_bold
    for j, h in enumerate(["状態", "点数", "仕入れ価格の合計", "店頭販売価格の合計"], 1):
        c = T.cell(r1, j, h)
        c.font, c.fill = f_head, fill_head
    for k, st in enumerate(["在庫", "出品中"]):
        r = r1 + 1 + k
        T.cell(r, 1, st)
        T.cell(r, 2, f'=COUNTIFS({LA},"個体",{LC("I")},$A{r})')
        T.cell(r, 3, f'=SUMIFS({LC("G")},{LA},"個体",{LC("I")},$A{r})')
        T.cell(r, 4, f'=SUMIFS({LC("H")},{LA},"個体",{LC("I")},$A{r})')
        for j in range(1, 5):
            T.cell(r, j).font, T.cell(r, j).border = f_norm, box
            if j >= 3:
                T.cell(r, j).number_format = YEN

    r2 = r1 + 5
    T.cell(r2 - 1, 1, "④ 販売月別の売上（台帳に販売日を入れると集計されます）").font = f_bold
    for j, h in enumerate(["販売月", "点数", "実販売額", "手数料・送料", "粗利"], 1):
        c = T.cell(r2, j, h)
        c.font, c.fill = f_head, fill_head
    y, m = 2026, 6
    for k in range(24):
        r = r2 + 1 + k
        T.cell(r, 1, date(y, m, 1)).number_format = "yyyy/mm"
        cond = f'{LC("L")},">="&$A{r},{LC("L")},"<"&EDATE($A{r},1)'
        T.cell(r, 2, f'=COUNTIFS({LA},"個体",{cond})')
        T.cell(r, 3, f'=SUMIFS({LC("K")},{LA},"個体",{cond})')
        T.cell(r, 4, f'=SUMIFS({LC("M")},{LA},"個体",{cond})')
        T.cell(r, 5, f'=SUMIFS({LC("N")},{LA},"個体",{cond})')
        for j in range(1, 6):
            T.cell(r, j).font, T.cell(r, j).border = f_norm, box
            if j >= 3:
                T.cell(r, j).number_format = YEN
        m += 1
        if m > 12:
            y, m = y + 1, 1
    for col, w in zip("ABCDEFGHIJK", (18, 14, 14, 14, 12, 18, 14, 10, 10, 10, 16)):
        T.column_dimensions[col].width = w
    T.row_dimensions[4].height = 32


def ensure_history(wb):
    if "納品書履歴" not in wb.sheetnames:
        H = wb.create_sheet("納品書履歴")
        H["A1"] = "納品書の登録履歴"
        H["A1"].font = f_title
        for j, h in enumerate(["登録日時", "仕入れ日", "仕入れ先", "納品書番号", "点数", "仕入れ合計（税込）", "納品書の合計"], 1):
            c = H.cell(3, j, h)
            c.font, c.fill = f_head, fill_head
        for col, w in zip("ABCDEFG", (18, 12, 22, 14, 8, 18, 14)):
            H.column_dimensions[col].width = w
    return wb["納品書履歴"]


def reorder(wb):
    order = ["まとめ", "前提", "通帳1", "通帳2", "台帳", "資材", "集計", "納品書履歴", "入力のしかた"]
    names = [n for n in order if n in wb.sheetnames] + [n for n in wb.sheetnames if n not in order]
    wb._sheets = [wb[n] for n in names]


# ---------- 計算 ----------
def yen(x):
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def calc_cost(unit, tax_included):
    return yen(unit) if tax_included else yen(Decimal(unit) * (1 + TAX_RATE))


def calc_list(cost):
    v = Decimal(cost) * MARKUP
    return int(math.floor(v / ROUND_UNIT) * ROUND_UNIT)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", nargs="?")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--book")
    ap.add_argument("--genus", action="store_true")
    ap.add_argument("--force", action="store_true", help="納品書の合計と合わなくても書き込む")
    a = ap.parse_args()
    book = find_book(a.book)
    wb = openpyxl.load_workbook(book)
    items, supplies = read_ledger(wb)

    if a.genus:
        g2v = {}
        for i in items:
            g2v.setdefault(i["genus"], set()).add(base_variety(i["variety"]))
        for g in sorted(g2v, key=kana_key):
            print(g + "：" + "、".join(sorted(g2v[g], key=kana_key)))
        return
    if not a.json:
        ap.error("納品書のJSONファイルを指定してください")

    with open(a.json, encoding="utf-8-sig") as f:
        d = json.load(f)
    supplier = d.get("仕入れ先") or ""
    no = str(d.get("納品書番号") or "")
    pdate = datetime.strptime(d["仕入れ日"], "%Y-%m-%d").date()
    month = pdate.strftime("%Y/%m")
    tax_inc = bool(d.get("税込表記", False))

    # 二重登録のチェック
    hist = wb["納品書履歴"] if "納品書履歴" in wb.sheetnames else None
    if hist is not None:
        for r in range(4, hist.max_row + 1):
            same_no = no and str(hist.cell(r, 4).value or "") == no and (hist.cell(r, 3).value or "") == supplier
            same_amt = (not no) and hist.cell(r, 2).value and to_date(hist.cell(r, 2).value) == pdate \
                and (hist.cell(r, 3).value or "") == supplier and hist.cell(r, 7).value == d.get("納品書合計")
            if same_no or same_amt:
                sys.exit("この納品書は、すでに登録されています（納品書履歴を確認してください）。")

    known = {}
    for i in items:
        known.setdefault(base_variety(i["variety"]), i["genus"])

    new_items, new_supplies, problems = [], [], []
    plan_rows = []
    total_cost = 0
    for k, it in enumerate(d["品目"], 1):
        cat = it.get("区分", "植物")
        qty = int(it.get("個数", 1))
        name = norm(it["品名"])
        cost = calc_cost(it["単価"], tax_inc)
        total_cost += cost * qty
        if cat in SUPPLY_CATS:
            label = name if cat in name else f"{cat} {name}"
            for _ in range(qty):
                new_supplies.append(dict(month=month, cat=cat, name=label, cost=cost))
            plan_rows.append((cat, label, qty, cost, None, ""))
            continue
        genus = it.get("属") or known.get(base_variety(name))
        if not genus:
            problems.append(f"{k}番目「{name}」の属名が分かりません（属を指定してください）")
            continue
        lst = it.get("店頭価格") or calc_list(cost)
        exist = [x for x in items + new_items if x["genus"] == genus and base_variety(x["variety"]) == name]
        # すでに同じ品種があるときは、番号のない既存の行にも番号を振り、続きの番号を使う
        top = max([x["no"] for x in exist if x["no"]], default=0)
        for x in [x for x in exist if not x["no"]]:
            top += 1
            x["no"] = top
        start = top + 1
        nums = []
        for q in range(qty):
            no_ = None if (qty == 1 and not exist) else start + q
            nums.append(no_)
            new_items.append(dict(genus=genus, variety=name, no=no_, month=month, date=pdate,
                                  note=(it.get("備考") or supplier or None), cost=cost, lst=lst,
                                  route=None, sold=None, sdate=None, fee=None))
        label_no = "" if nums[0] is None else (f"{nums[0]}" if len(nums) == 1 else f"{nums[0]}〜{nums[-1]}")
        plan_rows.append((genus, name, qty, cost, lst, label_no))
    if problems:
        sys.exit("\n".join(problems))

    print(f"仕入れ日 {pdate}／仕入れ先 {supplier}／納品書番号 {no or '-'}")
    print(f"{'属・区分':<10}{'品名':<22}{'個数':>4}{'仕入れ(税込)':>12}{'店頭たたき台':>12}  番号")
    for g, n_, q, c, l_, no_ in plan_rows:
        print(f"{g:<10}{n_:<22}{q:>4}{c:>12,}{(f'{l_:,}' if l_ else '-'):>12}  {no_}")
    print(f"仕入れ合計（税込）：{total_cost:,}円")
    inv = d.get("納品書合計")
    if inv is not None:
        diff = total_cost - int(inv)
        print(f"納品書の合計：{int(inv):,}円 → 差額 {diff:+,}円" + ("（一致）" if diff == 0 else "（要確認）"))
    if not a.apply:
        print("※確認のみです。台帳には書き込んでいません（--apply で書き込みます）。")
        return
    if inv is not None and total_cost != int(inv) and not a.force:
        sys.exit("納品書の合計と一致しないため、書き込みを止めました。品目や単価を確認してください（確認済みなら --force）。")

    # 書き込み前のバックアップ（直前の1つだけ残す）
    bak = os.path.join(os.path.dirname(book), "まるしかくベース事業計画_直前のバックアップ.xlsx")
    try:
        shutil.copy2(book, bak)
        write_sheets(wb, items + new_items, supplies + new_supplies)
        H = ensure_history(wb)
        H.append([datetime.now().strftime("%Y/%m/%d %H:%M"), pdate, supplier, no,
                  len(new_items) + len(new_supplies), total_cost, inv])
        r = H.max_row
        H.cell(r, 2).number_format = DATE
        for j in (6, 7):
            H.cell(r, j).number_format = YEN
        reorder(wb)
        wb.calculation.fullCalcOnLoad = True
        wb.save(book)
    except PermissionError:
        sys.exit("台帳を書き換えられません。Excelで開いている場合は閉じてから、もう一度実行してください。")
    print(f"台帳に追加しました（植物{len(new_items)}点、資材{len(new_supplies)}点）。")


if __name__ == "__main__":
    main()
