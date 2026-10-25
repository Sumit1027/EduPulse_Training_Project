import io
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_student_pdf_report(student_info, predicted_score, performance, recommendation, student_name="Student", student_id="N/A", key_factors=None):
    """
    Generates a formal academic PDF diagnostic report byte buffer.
    Returns bytes object.
    """
    buffer = io.BytesIO()
    
    if REPORTLAB_AVAILABLE:
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        styles = getSampleStyleSheet()
        
        # Custom Styles
        header_title_style = ParagraphStyle(
            'DocHeaderTitle',
            parent=styles['Heading1'],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#1E1B4B"),
            fontName='Helvetica-Bold'
        )
        
        header_sub_style = ParagraphStyle(
            'DocHeaderSub',
            parent=styles['Normal'],
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#64748B"),
            fontName='Helvetica'
        )
        
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#4F46E5"),
            fontName='Helvetica-Bold',
            spaceBefore=10,
            spaceAfter=6
        )
        
        body_style = ParagraphStyle(
            'BodyTextCustom',
            parent=styles['Normal'],
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#1F2937")
        )

        bold_label_style = ParagraphStyle(
            'BoldLabel',
            parent=body_style,
            fontName='Helvetica-Bold'
        )
        
        elements = []
        
        # Header Section
        elements.append(Paragraph("🎓 EduPulse Academic Performance & Diagnostic Report", header_title_style))
        elements.append(Paragraph("Official Academic Evaluation Document · EduPulse ML Platform", header_sub_style))
        elements.append(Spacer(1, 8))
        elements.append(HRFlowable(width="100%", thickness=2.5, color=colors.HexColor("#4F46E5"), spaceAfter=12))
        
        # Metadata Row Table
        meta_data = [
            [
                Paragraph(f"<b>Student Name:</b> {student_name}", body_style),
                Paragraph(f"<b>Student ID:</b> {student_id}", body_style),
                Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%d %B %Y')}", body_style)
            ]
        ]
        meta_table = Table(meta_data, colWidths=[200, 160, 180])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C7D2FE")),
            ('PADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 14))
        
        # Score Summary Card Box
        if predicted_score >= 80:
            badge_color = "#15803D" # Green
            badge_bg = "#DCFCE7"
            badge_text = "EXCELLENT PERFORMANCE (TIER 1)"
        elif predicted_score >= 60:
            badge_color = "#3730A3" # Indigo
            badge_bg = "#E0E7FF"
            badge_text = "GOOD ACADEMIC STANDING (TIER 2)"
        elif predicted_score >= 40:
            badge_color = "#B45309" # Amber
            badge_bg = "#FEF3C7"
            badge_text = "AVERAGE PERFORMANCE - NEEDS BOOST (TIER 3)"
        else:
            badge_color = "#B91C1C" # Red
            badge_bg = "#FEE2E2"
            badge_text = "HIGH RISK - ACADEMIC INTERVENTION REQUIRED (TIER 4)"
            
        summary_data = [
            [
                Paragraph(f"<font size=10 color='#64748B'><b>PREDICTED EXAM SCORE</b></font><br/><font size=24 color='{badge_color}'><b>{predicted_score:.2f} / 100</b></font>", body_style),
                Paragraph(f"<font size=10 color='#64748B'><b>RISK TIER & DIAGNOSIS</b></font><br/><font size=11 color='{badge_color}'><b>{badge_text}</b></font><br/><font size=9 color='#4B5563'>{performance}</font>", body_style)
            ]
        ]
        
        summary_table = Table(summary_data, colWidths=[240, 300])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(badge_bg)),
            ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor(badge_color)),
            ('PADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 14))
        
        # Recommendation Section
        elements.append(Paragraph("📌 Academic Action Plan & Interventions", section_style))
        rec_box_data = [[Paragraph(f"<b>Customized Guidance:</b> {recommendation}", body_style)]]
        rec_table = Table(rec_box_data, colWidths=[540])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
            ('PADDING', (0,0), (-1,-1), 10),
        ]))
        elements.append(rec_table)
        elements.append(Spacer(1, 14))
        
        # Student Feature Profile Table
        elements.append(Paragraph("📋 Input Feature Breakdown (19 Academic & Behavioral Factors)", section_style))
        
        profile_rows = [
            [
                Paragraph("<b>Factor Name</b>", bold_label_style),
                Paragraph("<b>Value</b>", bold_label_style),
                Paragraph("<b>Factor Name</b>", bold_label_style),
                Paragraph("<b>Value</b>", bold_label_style)
            ]
        ]
        keys = list(student_info.keys())
        
        for i in range(0, len(keys), 2):
            k1 = keys[i]
            v1 = str(student_info[k1])
            k2 = keys[i+1] if i+1 < len(keys) else ""
            v2 = str(student_info[k2]) if i+1 < len(keys) else ""
            
            k1_clean = k1.replace("_", " ")
            k2_clean = k2.replace("_", " ") if k2 else ""
            
            profile_rows.append([
                Paragraph(k1_clean, body_style),
                Paragraph(v1, body_style),
                Paragraph(k2_clean, body_style),
                Paragraph(v2, body_style)
            ])
            
        prof_table = Table(profile_rows, colWidths=[160, 110, 160, 110])
        prof_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#312E81")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FAFAFA")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('PADDING', (0,0), (-1,-1), 4.5),
        ]))
        
        elements.append(prof_table)
        elements.append(Spacer(1, 18))
        
        # Signatures & Verification Block
        sig_data = [
            [
                Paragraph("<b>Academic Counselor Signature:</b><br/><br/>___________________________", body_style),
                Paragraph("<b>Department Approval:</b><br/><br/>___________________________", body_style),
                Paragraph("<b>System Verification:</b><br/><br/>Validated by EduPulse ML Engine v1.0", body_style)
            ]
        ]
        sig_table = Table(sig_data, colWidths=[180, 180, 180])
        sig_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(KeepTogether([
            HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=10),
            sig_table,
            Spacer(1, 8),
            Paragraph("Official report automatically generated by <b>EduPulse Machine Learning System</b>. Confidential academic record.", header_sub_style)
        ]))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    else:
        # Fallback text representation if reportlab isn't installed
        text_report = f"""
        =====================================================
                 EDUPULSE STUDENT ACADEMIC REPORT
        =====================================================
        Student Name: {student_name}
        Student ID: {student_id}
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        PREDICTED EXAM SCORE: {predicted_score:.2f} / 100
        PERFORMANCE CATEGORY: {performance}
        RECOMMENDATION: {recommendation}
        
        STUDENT PROFILE DATA:
        """
        for k, v in student_info.items():
            text_report += f"  - {k.replace('_', ' ')}: {v}\n"
            
        text_report += "\n=====================================================\n"
        buffer.write(text_report.encode('utf-8'))
        buffer.seek(0)
        return buffer.getvalue()
