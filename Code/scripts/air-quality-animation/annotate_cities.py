#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import tkinter as tk
from tkinter import messagebox

# —— Configuration ——
JSON_DIR = 'cities_json'  # Directory containing JSON files for each city


# —— end Configuration ——

def compute_offset(pm25, year):
    """
    Calculate offset based on PM2.5 value and year, intelligently avoiding trend lines:

    Improved strategy: Based primarily on actual PM2.5 values rather than assuming fixed historical patterns
    Because industrialization and governance processes vary greatly across regions
    """
    # Horizontal offset: Adjusted by year to avoid crowding on the time axis
    if year < 1900:
        ox = -20  # Early years shift left
    elif year < 1950:
        ox = 5  # Mid-period years shift slightly right
    elif year < 2000:
        ox = -15  # Later years shift left
    else:
        ox = -25  # Modern years shift more left

    # Vertical offset: Mainly based on PM2.5 values, intelligently avoiding trend lines
    if pm25 <= 15:

        oy = 45
    elif pm25 <= 30:

        oy = 35
    elif pm25 <= 50:

        oy = 20
    elif pm25 <= 80:

        if year < 1950:
            oy = -25
        else:
            oy = 10
    elif pm25 <= 120:

        oy = -30
    else:

        oy = 40

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
        self.ent_search.pack(fill='x', pady=(0, 5))
        # Enter key acts the same as clicking Search
        self.ent_search.bind('<Return>', lambda e: self.do_search())

        tk.Button(frm, text="Search", command=self.do_search).pack(pady=(0, 5))

        self.lst_cities = tk.Listbox(frm, height=6)
        self.lst_cities.pack(fill='x')
        self.lst_cities.bind("<<ListboxSelect>>", self.on_city_select)

        # —— Details area (initially hidden) ——
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
        """Case-insensitive, ignores punctuation, checks if term is in s"""
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
            messagebox.showinfo("Info", "Please enter search keywords")
            return
        matched = [it for it in self.index
                   if self.safe_match(it['city'], term) or self.safe_match(it['country'], term)]
        if not matched:
            messagebox.showinfo("Info", "No matching city/country found")
            return
        self.populate_city_list(matched)

    def on_city_select(self, _):
        """After user selects a city, show details area and load existing bubbles for that city"""
        sel = self.lst_cities.curselection()
        if not sel:
            return
        it = self.curr_cities[sel[0]]
        self.selected = it
        self.lbl_sel.config(text=f"{it['city']}, {it['country']}")
        self.load_annotations()
        self.frm_det.pack(padx=10, pady=10, fill='both', expand=True)

    def back_to_search(self):
        """Return to search page, reset details area"""
        self.frm_det.pack_forget()
        self.lst_ann.delete(0, tk.END)
        self.ent_year.delete(0, 'end')
        self.txt_text.delete('1.0', 'end')
        self.btn_add.config(state='normal')
        self.btn_update.pack_forget()
        self.btn_delete.pack_forget()

    def load_annotations(self):
        """Load existing bubbles from JSON and populate the list"""
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
        """After selecting a bubble, fill input fields and switch to Update/Delete mode"""
        idx = self.lst_ann.curselection()
        if not idx:
            return
        a = self.obj.get('bubbles', [])[idx[0]]
        self.ent_year.delete(0, 'end');
        self.ent_year.insert(0, str(a['year']))
        self.txt_text.delete('1.0', 'end');
        self.txt_text.insert('1.0', a['text'])
        self.btn_add.config(state='disabled')
        self.btn_update.pack(side='left', padx=5)
        self.btn_delete.pack(side='left', padx=5)

    def add_annotation(self):
        """Add new bubble"""
        self._save_annotation(mode='add')

    def update_annotation(self):
        """Update existing bubble"""
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
        messagebox.showinfo("Done", f" {year} has been deleted")
        # Reload list and reset buttons
        self.load_annotations()
        self.btn_update.pack_forget()
        self.btn_delete.pack_forget()
        self.btn_add.config(state='normal')
        self.ent_year.delete(0, 'end')
        self.txt_text.delete('1.0', 'end')

    def _save_annotation(self, mode):
        """Internal: Add or update bubbles and write back to JSON"""
        try:
            year = int(self.ent_year.get().strip())
            text = self.txt_text.get('1.0', 'end').strip()
            if not text:
                raise ValueError
        except:
            messagebox.showerror("Error", "Please enter valid year and non-empty text")
            return

        # Find PM2.5 for that year
        pm25 = None
        for rec in self.obj.get('data', []):
            if rec.get('year') == year:
                pm25 = rec.get('value')
                break
        if pm25 is None:
            messagebox.showerror("Error", f"Data for year {year} does not exist")
            return

        ox, oy = compute_offset(pm25, year)
        ann = [a for a in self.obj.get('bubbles', []) if a['year'] != year]
        ann.append({'year': year, 'text': text, 'offset_x': ox, 'offset_y': oy})
        self.obj['bubbles'] = sorted(ann, key=lambda x: x['year'])
        self._write_json()
        messagebox.showinfo("Success",
                            f"{mode.title()} successful: {year}\noffset=({ox}, {oy})")
        # Reload and restore to add mode
        self.load_annotations()
        self.btn_update.pack_forget()
        self.btn_delete.pack_forget()
        self.btn_add.config(state='normal')
        self.ent_year.delete(0, 'end')
        self.txt_text.delete('1.0', 'end')

    def _write_json(self):
        """Write back to JSON file"""
        path = os.path.join(JSON_DIR, self.selected['fname'])
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.obj, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    root = tk.Tk()

    # —— Set initial window size and center it ——
    win_w, win_h = 600, 500
    root.update_idletasks()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w - win_w) // 2
    y = (screen_h - win_h) // 2
    root.geometry(f"{win_w}x{win_h}+{x}+{y}")

    App(root)
    root.mainloop()
