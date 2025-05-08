import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio
from mendel import generate_gametes, generate_filial

class MendelApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="purecanium-mendel")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = Gtk.ApplicationWindow(application=app)
        self.win.set_title("Mendel Calculator")
        self.win.set_default_size(400, 300)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_top=16, margin_bottom=16, margin_start=16, margin_end=16)
        self.win.set_child(vbox)

        self.entry1 = Gtk.Entry(placeholder_text="P1 Genotype")
        self.entry2 = Gtk.Entry(placeholder_text="P2 Genotype")
        vbox.append(self.entry1)
        vbox.append(self.entry2)

        self.checkbox = Gtk.CheckButton(label="Genotype Ratio")
        vbox.append(self.checkbox)

        self.entry1.connect("changed", self.on_input_change)
        self.entry2.connect("changed", self.on_input_change)

        self.matrix_grid = Gtk.Grid(column_spacing=8, row_spacing=8)
        vbox.append(self.matrix_grid)

        self.genotype_grid = Gtk.Grid(column_spacing=8, row_spacing=8)
        vbox.append(self.genotype_grid)

        self.implicit_phenotype_grid = Gtk.Grid(column_spacing=8, row_spacing=8)
        vbox.append(self.implicit_phenotype_grid)

        self.win.show()

    def on_input_change(self, entry):
        input1 = self.entry1.get_text()
        input2 = self.entry2.get_text()

        matrix, genotype, implicit_phenotypes = generate_filial(generate_gametes(input1), generate_gametes(input2))

        if len(input1) == len(input2):
            self.populate_matrix(matrix)
            self.populate_genotype_grid(genotype[0], genotype[1])
            self.populate_implicit_phenotype_grid(implicit_phenotypes[0], implicit_phenotypes[1])

    def populate_matrix(self, matrix):
        for child in list(self.matrix_grid):
            self.matrix_grid.remove(child)

        for row_idx, row in enumerate(matrix):
            for col_idx, value in enumerate(row):
                label = Gtk.Label(label=str(value))
                self.matrix_grid.attach(label, col_idx, row_idx, 1, 1)

    def populate_genotype_grid(self, row1, row2):
        for child in list(self.genotype_grid):
            self.genotype_grid.remove(child)

        for col_idx, value in enumerate(row1):
            label = Gtk.Label(label=str(value))
            self.genotype_grid.attach(label, col_idx, 0, 1, 1)

        for col_idx, value in enumerate(row2):
            label = Gtk.Label(label=str(value))
            self.genotype_grid.attach(label, col_idx, 1, 1, 1)

    def populate_implicit_phenotype_grid(self, row1, row2):
        for child in list(self.implicit_phenotype_grid):
            self.implicit_phenotype_grid.remove(child)

        for col_idx, value in enumerate(row1):
            label = Gtk.Label(label=str(value))
            self.implicit_phenotype_grid.attach(label, col_idx, 0, 1, 1)

        for col_idx, value in enumerate(row2):
            label = Gtk.Label(label=str(value))
            self.implicit_phenotype_grid.attach(label, col_idx, 1, 1, 1)

app = MendelApp()
app.run()