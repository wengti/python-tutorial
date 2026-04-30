from fpdf import FPDF
import pandas as pd

# lines parameters
num_of_lines_with_header = 26
bottom_h_with_header = 32
num_of_lines_without_header = 27
bottom_h_without_header = 20
line_height = 10

# Read csv file into a pd dataframe
df = pd.read_csv("topics.csv")

# Initialize the pdf
pdf = FPDF(
    orientation="portrait",
    format="A4",
)  # Default settings

pdf.set_auto_page_break(auto=False)
pdf.set_text_color(100, 100, 100)

for row in df.itertuples():

    # Add a new page
    pdf.add_page()

    # Header
    pdf.set_font(
        "Times",
        size=18,
        style="B",
    )
    pdf.cell(
        w=0,
        h=12,
        text=row[2],  # Can be row['Topic']
        border="B1",
    )

    # Lines
    for i in range(num_of_lines_with_header):
        height = bottom_h_with_header + i * line_height
        pdf.line(x1=10, y1=height, x2=200, y2=height)

    # Footer
    pdf.ln(h=((num_of_lines_with_header + 1) * line_height))
    pdf.set_font(
        "Times",
        size=8,
        style="BI",
    )
    pdf.cell(
        w=0,
        h=12,
        text=row[2],
        align="R",
    )

    for i in range(row[3] - 1):

        # Add a new page
        pdf.add_page()

        # Lines
        for i in range(num_of_lines_without_header):
            height = bottom_h_without_header + i * line_height
            pdf.line(x1=10, y1=height, x2=200, y2=height)

        # Footer
        pdf.ln(h=((num_of_lines_without_header) * line_height))
        pdf.set_font(
            "Times",
            size=8,
            style="BI",
        )
        pdf.cell(
            w=0,
            h=12,
            text=row[2],
            align="R",
        )


pdf.output("note.pdf")
