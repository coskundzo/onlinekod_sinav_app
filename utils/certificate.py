from flask import send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import io
import os

# Register Turkish-supporting fonts
try:
    # Try to register Arial (available on Windows)
    arial_path = "C:\\Windows\\Fonts\\arial.ttf"
    arial_bold_path = "C:\\Windows\\Fonts\\arialbd.ttf"
    
    if os.path.exists(arial_path):
        pdfmetrics.registerFont(TTFont('ArialUnicode', arial_path))
    if os.path.exists(arial_bold_path):
        pdfmetrics.registerFont(TTFont('ArialUnicode-Bold', arial_bold_path))
except:
    # Fallback to default fonts if Arial is not available
    pass

def generate_certificate(user, exam_attempt):
    """Generate a PDF certificate for the exam"""
    buffer = io.BytesIO()
    
    # Create PDF
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()
    
    # Determine which font to use (with Turkish support)
    try:
        main_font = 'ArialUnicode'
        bold_font = 'ArialUnicode-Bold'
    except:
        main_font = 'Helvetica'
        bold_font = 'Helvetica-Bold'
    
    # Custom styles with Turkish font support
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=24,
        textColor=colors.HexColor('#0066CC'),  # onlinekod.com blue
        alignment=TA_CENTER,
        fontName=bold_font,
        spaceAfter=8
    )
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName=bold_font
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName=main_font
    )
    
    text_style = ParagraphStyle(
        'CustomText',
        parent=styles['Normal'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName=main_font
    )
    
    # Add onlinekod.com header
    elements.append(Spacer(1, 0.2*inch))
    
    # Try to add logo if available
    logo_path = os.path.join('static', 'images', 'onlinekod_logo.png')
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=2*inch, height=0.6*inch, kind='proportional')
            elements.append(logo)
            elements.append(Spacer(1, 0.1*inch))
        except:
            # If logo fails, show text header
            elements.append(Paragraph("<b>ONLINEKOD.COM</b>", header_style))
    else:
        # No logo file, use text header
        elements.append(Paragraph("<b>ONLINEKOD.COM</b>", header_style))
    
    elements.append(Paragraph("Bursluluk Sınavı", subtitle_style))
    
    # Add decorative line
    line_data = [['━' * 100]]
    line_table = Table(line_data, colWidths=[7.5*inch])
    line_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#0066CC')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Certificate title
    elements.append(Paragraph("🏆 BAŞARI SERTİFİKASI 🏆", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("Bu sertifika ile onaylanır ki,", subtitle_style))
    elements.append(Spacer(1, 0.2*inch))
    
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Normal'],
        fontSize=28,
        textColor=colors.HexColor('#2980b9'),
        alignment=TA_CENTER,
        fontName=bold_font
    )
    elements.append(Paragraph(f"<b>{user.username}</b>", name_style))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph(
        f"onlinekod.com Bursluluk Sınavı'nı başarıyla tamamlamıştır.",
        text_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Results table
    level_name = {
        'advanced': 'İleri Seviye 🔴',
        'intermediate': 'Orta Seviye 🟡',
        'beginner': 'Başlangıç Seviyesi 🟢',
        'none': 'Kategori Dışı ⚪'
    }
    
    data = [
        ['Puan', 'Seviye', 'Tarih'],
        [
            f"{exam_attempt.score:.1f}/100",
            level_name.get(exam_attempt.get_level(), 'N/A'),
            exam_attempt.end_time.strftime('%d/%m/%Y')
        ]
    ]
    
    table = Table(data, colWidths=[2*inch, 3*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), bold_font),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), main_font),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Add footer with onlinekod.com branding
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER,
        fontName=main_font
    )
    
    brand_footer_style = ParagraphStyle(
        'BrandFooter',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#0066CC'),
        alignment=TA_CENTER,
        fontName=bold_font,
        spaceAfter=4
    )
    
    elements.append(Paragraph(
        f"Sertifika No: OK-{exam_attempt.id}-{user.id}-{datetime.now().year}",
        footer_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>www.onlinekod.com</b>", brand_footer_style))
    elements.append(Paragraph("Kodlama Eğitimi ve Bursluluk Sınavları", footer_style))
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'certificate_{user.username}_{exam_attempt.id}.pdf'
    )
