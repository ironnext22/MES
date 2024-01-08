

def zapis_do_vtk(x_values, y_values, cells, values, output_filename):
    vertices = [[x, y, 0.0] for x, y in zip(x_values, y_values)]
    vertices = vertices[::-1]
    vtk_content = "# vtk DataFile Version 2.0\n"
    vtk_content += "MES Results\n"
    vtk_content += "ASCII\n"
    vtk_content += "DATASET UNSTRUCTURED_GRID\n\n"

    num_vertices = len(vertices)
    vtk_content += f"POINTS {num_vertices} float\n"
    for vertex in vertices:
        vtk_content += f"{vertex[0]} {vertex[1]} {vertex[2]}\n"

    vtk_content += "\n"

    num_cells = len(cells)
    total_cell_count = sum(len(cell) + 1 for cell in cells)
    vtk_content += f"CELLS {num_cells} {total_cell_count}\n"
    for cell in cells:
        vtk_content += f"4 {' '.join(str(int(v-1)) for v in cell)}\n"

    vtk_content += "\n"

    vtk_content += f"CELL_TYPES {num_cells}\n"
    for _ in range(num_cells):
        vtk_content += "9\n"  # 9 oznacza quad

    vtk_content += "\n"

    vtk_content += f"POINT_DATA {num_vertices}\n"
    vtk_content += "SCALARS Temp float 1\n"
    vtk_content += "LOOKUP_TABLE default\n"
    for value in values:
        vtk_content += f"{value}\n"

    # Zapisanie zawartości do pliku
    with open(output_filename, "w") as vtk_file:
        vtk_file.write(vtk_content)