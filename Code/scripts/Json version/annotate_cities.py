#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import tkinter as tk
from tkinter import messagebox

# —— Configuration ——
JSON_DIR = 'cities_json'   # Directory to store JSON files for each city
# —— end Configuration ——

def compute_offset(pm25, year):
    """
    Compute offset based on PM2.5 value and year (example heuristic strategy):
      - Initial horizontal offset ox=5;
      - If 2000–2010: ox-=15; if >2010: ox-=25; if <2000: unchanged;
      - Vertical offset oy: if PM2.5 > 60 then -10, else +10.
    """
    ox = 5
    if 2000 <= year <= 2010:
        ox -= 15
    elif year > 2010:
        ox -= 25
    oy = -10 if pm25 > 60 else 10
    return ox, oy

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("City Annotation Tool")

        # —— Load all city indices ——
        self.index = []
        for fname in os.listdir(JSON_DIR):
            if not fname.endswith('.json'):
                continue
            try:
                obj = json.load(open(os.path.join(JSON_DIR, fname), 'r', encoding='utf-8'))
                self.index.append({
                    'fname': fname,
                    'city': obj.get('city', ''),
                    'country': obj.get('country', '')
                })
            except Exception:
                pass

        # —— Search area ——
        frm = tk.Frame(root)
        frm.pack(padx=10, pady=5, fill='x')

        tk.Label(frm, text="Search city or country:").pack(anchor='w')
        self.ent_search = tk.Entry(frm)
        self.ent_search.pack(fill='x', pady=(0,5))
        # Enter key is equivalent to clicking Search
        self.ent_search.bind('<Return>', lambda e: self.do_search())

        tk.Button(frm, text="Search", command=self.do_search).pack(pady=(0,5))

        self.lst_cities = tk.Listbox(frm, height=6)
        self.lst_cities.pack(fill='x')
        self.lst_cities.bind("<<ListboxSelect>>", self.on_city_select)

        # —— Detail area (initially hidden) ——
        self.frm_det = tk.Frame(root)

        # Selected city
        tk.Label(self.frm_det, text="Selected:").grid(row=0, column=0, sticky='w')
        self.lbl_sel = tk.Label(self.frm_det, text="(none)", font=('Arial', 12, 'bold'))
        self.lbl_sel.grid(row=0, column=1, sticky='w', padx=5)

        # Year input
        tk.Label(self.frm_det, text="Year:").grid(row=1, column=0, sticky='e')
        self.ent_year = tk.Entry(self.frm_det, width=10)
        self.ent_year.grid(row=1, column=1, sticky='w')

        # Text input
        tk.Label(self.frm_det, text="Text:").grid(row=2, column=0, sticky='ne')
        self.txt_text = tk.Text(self.frm_det, width=40, height=4)
        self.txt_text.grid(row=2, column=1, pady=2)

        # Button area
        btn_frm = tk.Frame(self.frm_det)
        btn_frm.grid(row=3, column=0, columnspan=2, pady=5)
        self.btn_add = tk.Button(btn_frm, text="Add", width=10, command=self.add_annotation)
        self.btn_add.pack(side='left', padx=5)
        self.btn_update = tk.Button(btn_frm, text="Update", width=10, command=self.update_annotation)
        self.btn_delete = tk.Button(btn_frm, text="Delete", width=10, command=self.delete_annotation)
        self.btn_back = tk.Button(btn_frm, text="Back", width=10, command=self.back_to_search)
        self.btn_back.pack(side='left', padx=5)

        # Existing bubbles list
        tk.Label(self.frm_det, text="Existing bubbles:").grid(row=4, column=0, sticky='nw')
        self.lst_ann = tk.Listbox(self.frm_det, width=40, height=6)
        self.lst_ann.grid(row=4, column=1, sticky='w')
        self.lst_ann.bind("<<ListboxSelect>>", self.on_ann_select)

        self.frm_det.pack_forget()
        self.populate_city_list(self.index)

    def safe_match(self, s, term):
        """Case-insensitive, punctuation-agnostic check if term is in s"""
        return term in re.sub(r'[^\w]', ' ', s.lower())

    def populate_city_list(self, items):
        """Display search results in the city list"""
        self.lst_cities.delete(0, tk.END)
        for it in items:
            self.lst_cities.insert(tk.END, f"{it['city']}, {it['country']}")
        self.curr_cities = items

    def do_search(self):
        """Handle search action"""
        term = self.ent_search.get().strip().lower()
        if not term:
            messagebox.showinfo("Info", "Please enter a search keyword")
            return
        matched = [it for it in self.index
                   if self.safe_match(it['city'], term) or self.safe_match(it['country'], term)]
        if not matched:
            messagebox.showinfo("Info", "No matching city/country found")
            return
        self.populate_city_list(matched)

    def on_city_select(self, _):
        """After a city is selected, show detail area and load its existing bubbles"""
        sel = self.lst_cities.curselection()
        if not sel:
            return
        it = self.curr_cities[sel[0]]
        self.selected = it
        self.lbl_sel.config(text=f"{it['city']}, {it['country']}")
        self.load_annotations()
        self.frm_det.pack(padx=10, pady=10, fill='both', expand=True)

    def back_to_search(self):
        """Return to search view and reset detail area"""
        self.frm_det.pack_forget()
        self.lst_ann.delete(0, tk.END)
        self.ent_year.delete(0, 'end')
        self.txt_text.delete('1.0', 'end')
        self.btn_add.config(state='normal')
        self.btn_update.pack_forget()
        self.btn_delete.pack_forget()

    def load_annotations(self):
        """Load existing bubbles from JSON and populate list"""
        path = os.path.join(JSON_DIR, self.selected['fname'])
        with open(path, 'r', encoding='utf-8') as f:
            self.obj = json.load(f)
        ann = self.obj.get('bubbles', [])
        self.lst_ann.delete(0, tk.END)
        for a in ann:
            txt = a['text']
            short = txt if len(txt) <= 30 else txt[:30] + '...'
            self.lst_ann.insert(tk.END, f"{a['year']} → {short}")

    def on_ann_select(self, _):
        """Fill inputs when a bubble is selected, and switch to Update/Delete"""
        idx = self.lst_ann.curselection()
        if not idx:
            return
        a = self.obj.get('bubbles', [])[idx[0]]
        self.ent_year.delete(0, 'end'); self.ent_year.insert(0, str(a['year']))
        self.txt_text.delete('1.0', 'end'); self.txt_text.insert('1.0', a['text'])
        self.btn_add.config(state='disabled')
        self.btn_update.pack(side='left', padx=5)
        self.btn_delete.pack(side='left', padx=5)

    def add_annotation(self):
        """Add a new bubble"""
        self._save_annotation(mode='add')

    def update_annotation(self):
        """Update an existing bubble"""
        self._save_annotation(mode='update')

    def delete_annotation(self):
        """Delete selected bubble"""
        try:
            year = int(self.ent_year.get().strip())
        except:
            return
        ann = [a for a in self.obj.get('bubbles', []) if a['year'] != year]
        self.obj['bubbles'] = sorted(ann, key=lambda x: x['year'])
        self._write_json()
        messagebox.showinfo("Done", f"Bubble for {year} deleted.")
        self.load_annotations()
        self.btn_update.pack_forget()
        self.btn_delete.pack_forget()
        self.btn_add.config(state='normal')
        self.ent_year.delete(0, 'end')
        self.txt_text.delete('1.0', 'end')

    def _save_annotation(self, mode):
        """Internal: add or update bubbles and write back to JSON"""
        try:
            year = int(self.ent_year.get().strip())
            text = self.txt_text.get('1.0', 'end').strip()
            if not text:
                raise ValueError
        except:
            messagebox.showerror("Error", "Please enter a valid year and non-empty text")
            return

        # Find PM2.5 for the year
        pm25 = None
        for rec in self.obj.get('data', []):
            if rec.get('year') == year:
                pm25 = rec.get('value')
                break
        if pm25 is None:
            messagebox.showerror("Error", f"No data found for year {year}")
            return

        ox, oy = compute_offset(pm25, year)
        ann = [a for a in self.obj.get('bubbles', []) if a['year'] != year]
        ann.append({'year': year, 'text': text, 'offset_x': ox, 'offset_y': oy})
        self.obj['bubbles'] = sorted(ann, key=lambda x: x['year'])
        self._write_json()
        messagebox.showinfo("Success",
                            f"{mode.title()} successful: {year}\noffset=({ox}, {oy})")
        self.load_annotations()
        self.btn_update.pack_forget()
        self.btn_delete.pack_forget()
        self.btn_add.config(state='normal')
        self.ent_year.delete(0, 'end')
        self.txt_text.delete('1.0', 'end')

    def _write_json(self):
        """Write JSON file back"""
        path = os.path.join(JSON_DIR, self.selected['fname'])
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.obj, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    root = tk.Tk()

    # —— Set initial window size and center ——
    win_w, win_h = 600, 500
    root.update_idletasks()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w - win_w) // 2
    y = (screen_h - win_h) // 2
    root.geometry(f"{win_w}x{win_h}+{x}+{y}")

    App(root)
    root.mainloop()
