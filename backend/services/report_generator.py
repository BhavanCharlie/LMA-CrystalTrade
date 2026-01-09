from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from typing import Dict
import os
from datetime import datetime


class ReportGenerator:
    def __init__(self):
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)

    async def generate_report(self, analysis, report_type: str = "executive") -> str:
        """Generate PDF report"""
        filename = f"{analysis.id}_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#0ea5e9"),
            spaceAfter=30,
            alignment=TA_CENTER,
        )
        story.append(Paragraph("Due Diligence Report", title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Loan Information
        story.append(Paragraph(f"Loan: {analysis.loan_name}", styles["Heading2"]))
        story.append(Paragraph(f"Analysis ID: {analysis.id}", styles["Normal"]))
        story.append(
            Paragraph(
                f"Date: {analysis.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 0.3 * inch))
        
        # Risk Score
        if analysis.risk_score is not None:
            story.append(Paragraph("Risk Assessment", styles["Heading2"]))
            risk_color = (
                colors.red
                if analysis.risk_score >= 70
                else colors.orange
                if analysis.risk_score >= 40
                else colors.green
            )
            story.append(
                Paragraph(
                    f"Overall Risk Score: <b>{analysis.risk_score}/100</b>",
                    ParagraphStyle(
                        "RiskScore",
                        parent=styles["Normal"],
                        textColor=risk_color,
                        fontSize=16,
                    ),
                )
            )
            
            if analysis.risk_breakdown:
                breakdown = analysis.risk_breakdown
                risk_data = [
                    ["Category", "Score"],
                    ["Credit Risk", f"{breakdown.get('credit_risk', 0)}/100"],
                    ["Legal Risk", f"{breakdown.get('legal_risk', 0)}/100"],
                    ["Operational Risk", f"{breakdown.get('operational_risk', 0)}/100"],
                ]
                risk_table = Table(risk_data, colWidths=[3 * inch, 2 * inch])
                risk_table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, 0), 12),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                            ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ]
                    )
                )
                story.append(risk_table)
            story.append(Spacer(1, 0.3 * inch))
        
        # Compliance Checks
        if analysis.compliance_checks:
            story.append(Paragraph("Compliance Checklist", styles["Heading2"]))
            for check in analysis.compliance_checks:
                status_color = (
                    colors.green
                    if check["status"] == "pass"
                    else colors.red
                    if check["status"] == "fail"
                    else colors.orange
                )
                status_text = check["status"].upper()
                story.append(
                    Paragraph(
                        f"<b>{check['category']}</b> - <font color='{status_color.hex}'>[{status_text}]</font>",
                        styles["Normal"],
                    )
                )
                story.append(
                    Paragraph(f"{check['description']}", styles["Normal"])
                )
                if check.get("details"):
                    story.append(
                        Paragraph(f"Details: {check['details']}", styles["Normal"])
                    )
                story.append(Spacer(1, 0.1 * inch))
            story.append(Spacer(1, 0.2 * inch))
        
        # Extracted Terms
        if analysis.extracted_terms:
            story.append(Paragraph("Key Loan Terms", styles["Heading2"]))
            terms = analysis.extracted_terms
            if terms.get("interest_rate"):
                story.append(
                    Paragraph(f"Interest Rate: {terms['interest_rate']}", styles["Normal"])
                )
            if terms.get("maturity_date"):
                story.append(
                    Paragraph(f"Maturity Date: {terms['maturity_date']}", styles["Normal"])
                )
            if terms.get("principal_amount"):
                story.append(
                    Paragraph(
                        f"Principal Amount: {terms['principal_amount']}", styles["Normal"]
                    )
                )
            story.append(Spacer(1, 0.2 * inch))
        
        # Recommendations
        if analysis.recommendations:
            story.append(Paragraph("Recommendations", styles["Heading2"]))
            for i, rec in enumerate(analysis.recommendations, 1):
                story.append(
                    Paragraph(f"{i}. {rec}", styles["Normal"])
                )
            story.append(Spacer(1, 0.2 * inch))
        
        # Footer
        story.append(Spacer(1, 0.5 * inch))
        story.append(
            Paragraph(
                f"Generated by CrystalTrade on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                ParagraphStyle(
                    "Footer",
                    parent=styles["Normal"],
                    fontSize=8,
                    textColor=colors.grey,
                    alignment=TA_CENTER,
                ),
            )
        )
        
        doc.build(story)
        return filepath

