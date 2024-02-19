from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import runner

exploratory_data_analysis_response = runner.exploritory_data_analysis()

def main():
    pass


def build_pdf_report(exploratory_data_analysis_response, analysis_technique_response, df):
    # Create a PDF report
    pdf_file = "output_document.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    # Styles for the document
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    # List to add content
    content = []

    # Adding a paragraph
    content.append(Paragraph("This is a paragraph with some JSON output:", normal_style))
    content.append(Spacer(1, 12))

    # Suppose this is your JSON data formatted as a string for simplicity
    json_data = "{'key': 'value', 'list': [1, 2, 3]}"
    content.append(Paragraph(json_data, normal_style))
    content.append(Spacer(1, 12))

    # Adding an image (e.g., a saved graph)
    graph_image = "path_to_your_graph_image.png"
    content.append(Image(graph_image, width=200, height=150))

    # Build the PDF
    doc.build(content)



if __name__ == "__main__":
    main()