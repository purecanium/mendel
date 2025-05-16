import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from mendel import generate_gametes, generate_filial, generate_expl_phenotypes

GRID_PADDING = 8
TAB_PADDING = 4

class MendelApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.purecanium.mendel")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = Gtk.ApplicationWindow(application=app)
        self.win.set_title("Mendel Calculator")
        self.win.set_default_size(380, 600)

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.win.set_child(main_vbox)

        tab_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        tab_header.set_hexpand(True)
        tab_header.set_margin_top(TAB_PADDING)
        tab_header.set_margin_bottom(0)
        tab_header.set_margin_start(TAB_PADDING)
        tab_header.set_margin_end(TAB_PADDING)
        main_vbox.append(tab_header)

        self.btn_gen = Gtk.ToggleButton(label="Genotype")
        self.btn_pheno = Gtk.ToggleButton(label="Phenotype")
        for btn in (self.btn_gen, self.btn_pheno):
            btn.set_hexpand(True)
            btn.set_margin_start(TAB_PADDING)
            btn.set_margin_end(TAB_PADDING)
            btn.set_margin_top(TAB_PADDING)
            btn.set_margin_bottom(0)
            btn.get_style_context().add_class("flat")
            tab_header.append(btn)

        self.btn_gen.set_active(True)
        self.btn_gen.connect("toggled", self.on_tab_toggled)
        self.btn_pheno.connect("toggled", self.on_tab_toggled)

        self.stack = Gtk.Stack()
        main_vbox.append(self.stack)

        ### Genotype Tab
        geno_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
            margin_top=8, margin_bottom=8,
            margin_start=8, margin_end=8,
        )
        self.stack.add_named(geno_box, "genotype")

        lbl_geno = Gtk.Label(label="Parental Genotype")
        lbl_geno.set_xalign(0)
        lbl_geno.get_style_context().add_class("heading")
        geno_box.append(lbl_geno)

        self.P1Genotype = Gtk.Entry(placeholder_text="P1 Genotype")
        self.P2Genotype = Gtk.Entry(placeholder_text="P2 Genotype")
        self.chk   = Gtk.CheckButton(label="Show genotype ratios")
        for w in (self.P1Genotype, self.P2Genotype, self.chk):
            geno_box.append(w)

        self.matrix_grid    = self.make_padded_grid()
        self.genotype_grid  = self.make_padded_grid()
        self.phenotype_grid = self.make_padded_grid()

        geno_box.append(self.make_matrix_section("Punnett Square", self.matrix_grid))
        self.geno_sec = self.make_scrollable_framed_section("Filial Genotype", self.genotype_grid)
        self.pheno_sec= self.make_scrollable_framed_section("Filial Implicit Phenotype", self.phenotype_grid, initial_height=40)
        for sec in (self.geno_sec, self.pheno_sec):
            geno_box.append(sec)

        for widget in (self.P1Genotype, self.P2Genotype):
            widget.connect("changed", self.on_input_change)
        self.chk.connect("toggled", self.on_chk_toggle)

        self.geno_sec.set_visible(False)

        ### Phenotype Tab
        pheno_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
            margin_top=8, margin_bottom=8,
            margin_start=8, margin_end=8,
        )
        self.stack.add_named(pheno_box, "phenotype")

        self.lbl_phn = Gtk.Label(label="Allele's Assosiated Phenotypes")
        self.lbl_phn.set_xalign(0)
        self.lbl_phn.get_style_context().add_class("heading")
        pheno_box.append(self.lbl_phn)
        self.lbl_phn.set_visible(False)

        self.ExplicitBox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )
        pheno_box.append(self.ExplicitBox)

        self.explicit_pheno_grid = self.make_padded_grid()
        self.explicit_pheno_sec = self.make_scrollable_framed_section("Explicit Phenotypes", self.explicit_pheno_grid)
        self.explicit_pheno_sec.set_visible(False)
        pheno_box.append(self.explicit_pheno_sec)

        self.win.show()
        self.on_input_change(None)

    def on_tab_toggled(self, btn):
        if btn == self.btn_gen and btn.get_active():
            self.btn_pheno.set_active(False)
            self.stack.set_visible_child_name("genotype")
        elif btn == self.btn_pheno and btn.get_active():
            self.btn_gen.set_active(False)
            self.stack.set_visible_child_name("phenotype")

    def make_padded_grid(self):
        g = Gtk.Grid(column_spacing=8, row_spacing=8)
        g.set_margin_top(GRID_PADDING)
        g.set_margin_bottom(GRID_PADDING)
        g.set_margin_start(GRID_PADDING)
        g.set_margin_end(GRID_PADDING)
        return g

    def make_matrix_section(self, title, grid):
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        lbl   = Gtk.Label(label=title)
        lbl.set_xalign(0)
        lbl.get_style_context().add_class("heading")
        outer.append(lbl)

        frame = Gtk.Frame()
        frame.set_hexpand(True); frame.set_vexpand(True)
        frame.get_style_context().add_class("frame")

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_child(grid)
        scroll.set_hexpand(True); scroll.set_vexpand(True)

        frame.set_child(scroll)
        outer.append(frame)
        return outer

    def make_scrollable_framed_section(self, title, grid, initial_height=None):
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        lbl   = Gtk.Label(label=title)
        lbl.set_xalign(0)
        lbl.get_style_context().add_class("heading")
        outer.append(lbl)

        frame = Gtk.Frame()
        frame.get_style_context().add_class("frame")
        if initial_height:
            frame.set_size_request(-1, initial_height)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        scroll.set_child(grid)
        scroll.set_hexpand(True)

        frame.set_child(scroll)
        outer.append(frame)
        return outer

    def on_input_change(self, *_):
        p1, p2 = self.P1Genotype.get_text(), self.P2Genotype.get_text()
        if not p1 or not p2 or len(p1) != len(p2): return
        matrix, self.geno, self.impl_pheno, self.loci = generate_filial(generate_gametes(p1), generate_gametes(p2))
        self.populate_matrix(matrix)
        self.populate_two_row_grid(self.phenotype_grid, self.impl_pheno)
        self.populate_two_row_grid(self.genotype_grid, self.geno)
        self.build_explicit_entries(self.loci)
        for c in list(self.explicit_pheno_grid): self.explicit_pheno_grid.remove(c)
        self.explicit_pheno_sec.set_visible(False)

    def on_chk_toggle(self, *_):
        if self.chk.get_active():
            self.geno_sec.set_visible(True)
        else:
            self.geno_sec.set_visible(False)

    def populate_matrix(self, matrix):
        for c in list(self.matrix_grid): self.matrix_grid.remove(c)
        for r, row in enumerate(matrix):
            for c, val in enumerate(row):
                lbl = Gtk.Label(); txt = str(val)
                if r==0 or c==0:
                    lbl.set_use_markup(True); lbl.set_markup(f"<b>{txt}</b>")
                else:
                    lbl.set_text(txt)
                lbl.set_halign(Gtk.Align.CENTER); lbl.set_valign(Gtk.Align.CENTER)
                self.matrix_grid.attach(lbl, c, r, 1, 1)

    def populate_two_row_grid(self, grid, rows):
        for c in list(grid): grid.remove(c)
        for col, v in enumerate(rows[0]): grid.attach(Gtk.Label(label=str(v)), col, 0, 1, 1)
        for col, v in enumerate(rows[1]): grid.attach(Gtk.Label(label=str(v)), col, 1, 1, 1)

    def build_explicit_entries(self, loci):
        for w in list(self.ExplicitBox):
            self.ExplicitBox.remove(w)
        self.lbl_phn.set_visible(True)

        self.explicit_entries = []

        for loc in loci:
            dom_e = Gtk.Entry(placeholder_text=f"{loc}")
            rec_e = Gtk.Entry(placeholder_text=f"{loc.lower()}")
            dom_e.connect("changed", self.on_explicit_changed)
            rec_e.connect("changed", self.on_explicit_changed)

            self.ExplicitBox.append(dom_e)
            self.ExplicitBox.append(rec_e)
            self.explicit_entries.extend([dom_e, rec_e])

    def on_explicit_changed(self, *_):
        labels = [e.get_text() for e in self.explicit_entries]
        if all(labels):
            exp = generate_expl_phenotypes(self.loci, self.impl_pheno, labels)
        self.populate_two_row_grid(self.explicit_pheno_grid, exp)
        self.explicit_pheno_sec.set_visible(True)

if __name__ == '__main__':
    app = MendelApp()
    app.run()