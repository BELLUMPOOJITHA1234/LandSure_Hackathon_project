from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models.users import User
from app.models.documents import Document
from app.models.land_records import LandRecord
from app.models.validation import ValidationResult
from app.models.audit import AuditLog
from app.dependencies import get_password_hash
import datetime

def seed_database():
    # 1. Initialize tables
    init_db()
    
    db = SessionLocal()
    try:
        # Check if users already exist
        if db.query(User).filter(User.username == "revenue_officer").first():
            print("Database already seeded. Skipping seeder.")
            return

        print("Seeding database...")

        # 2. Seed Users
        officer = User(
            username="revenue_officer",
            email="officer@revenue.gov.in",
            hashed_password=get_password_hash("sih2026password"),
            role="Official",
            is_active=True
        )
        admin = User(
            username="admin_sih",
            email="admin@revenue.gov.in",
            hashed_password=get_password_hash("sih2026admin"),
            role="Admin",
            is_active=True
        )
        db.add(officer)
        db.add(admin)
        db.flush() # Secure IDs

        # 3. Seed Document 1: English Survey Record (Verified)
        doc1 = Document(
            original_filename="english_survey_sample.png",
            file_path="uploads/english_survey_sample.png",
            preprocessed_path="/static/preprocessed/preprocessed_english_survey_sample.png",
            doc_type="Survey Record",
            language="English",
            format_type="Printed",
            status="Verified",
            confidence_score=95.4,
            ocr_text="""
            Government of Andhra Pradesh - Land Revenue Department
            RECORD OF RIGHTS (ROR) - Form I-B
            District: West Godavari
            Tehsil/Mandal: Pedapadu
            Village: Krishnapuram
            Survey Number: 145/3A
            Khasra Number: KH/99201
            Khata Number: 412
            Plot Number: 12
            Area/Extent: 2.50 Acres
            Land Classification: Dry - Agricultural
            Ownership Type: Pattadar (Self)
            Owner Name: Kondru Ramu
            Registration Number: 2401/2024
            Registration Date: 12-04-2024
            """,
            created_at=datetime.datetime.utcnow() - datetime.timedelta(days=10)
        )
        db.add(doc1)
        db.flush()

        rec1 = LandRecord(
            document_id=doc1.id,
            owner_name="Kondru Ramu",
            survey_number="145/3A",
            khasra_number="KH/99201",
            khata_number="412",
            plot_number="12",
            area=2.50,
            area_unit="Acres",
            village="Krishnapuram",
            tehsil_mandal="Pedapadu",
            district="West Godavari",
            land_classification="Dry - Agricultural",
            ownership_type="Pattadar",
            registration_number="2401/2024",
            registration_date="12-04-2024",
            confidence_scores={
                "owner_name": 95.0, "survey_number": 95.0, "area": 95.0, 
                "village": 95.0, "tehsil_mandal": 95.0, "district": 95.0
            },
            verification_status="Verified",
            created_at=doc1.created_at,
            updated_at=doc1.created_at
        )
        db.add(rec1)
        db.flush()

        # 4. Seed Document 2: Telugu Adangal (Verified)
        doc2 = Document(
            original_filename="telugu_adangal_sample.jpg",
            file_path="uploads/telugu_adangal_sample.jpg",
            preprocessed_path="/static/preprocessed/preprocessed_telugu_adangal_sample.png",
            doc_type="Pattadar/Land Ownership Record",
            language="Telugu",
            format_type="Printed",
            status="Verified",
            confidence_score=92.1,
            ocr_text="""
            ఆంధ్రప్రదేశ్ ప్రభుత్వం - భూ రెవెన్యూ విభాగం
            గ్రామ ఖాతా నంబరు 3 - అడంగల్ / పహానీ
            గ్రామం: కృష్ణపురం (Krishnapuram)
            మండలం: పెదపాడు (Pedapadu)
            జిల్లా: పశ్చిమ గోదావరి (West Godavari)
            ఖాతా సంఖ్య (Khata Number): 412
            పట్టాదారు పేరు (Owner Name): కొండ్రు రాము (Kondru Ramu)
            సర్వే నంబరు (Survey Number): 145/3A
            విస్తీర్ణం (Area/Extent): 2.50 ఎకరాలు (Acres)
            భూమి వర్గీకరణ (Classification): మెట్ట (Dry - Agricultural)
            """,
            created_at=datetime.datetime.utcnow() - datetime.timedelta(days=9)
        )
        db.add(doc2)
        db.flush()

        rec2 = LandRecord(
            document_id=doc2.id,
            owner_name="Kondru Ramu",
            survey_number="145/3A",
            khasra_number="KH/99201",
            khata_number="412",
            plot_number="12",
            area=2.50,
            area_unit="Acres",
            village="Krishnapuram",
            tehsil_mandal="Pedapadu",
            district="West Godavari",
            land_classification="Dry - Agricultural",
            ownership_type="Pattadar",
            confidence_scores={
                "owner_name": 91.0, "survey_number": 93.0, "area": 95.0,
                "village": 90.0, "tehsil_mandal": 92.0, "district": 94.0
            },
            verification_status="Verified",
            regional_values={
                "owner_name": "కొండ్రు రాము",
                "village": "కృష్ణపురం",
                "tehsil_mandal": "పెదపాడు",
                "district": "పశ్చిమ గోదావరి",
                "land_classification": "మెట్ట",
                "ownership_type": "పట్టాదారు"
            },
            created_at=doc2.created_at,
            updated_at=doc2.created_at
        )
        db.add(rec2)
        db.flush()

        # 5. Seed Document 3: Owner Conflict Record (Status: Owner Conflict)
        doc3 = Document(
            original_filename="conflict_owner_sample.png",
            file_path="uploads/conflict_owner_sample.png",
            preprocessed_path="/static/preprocessed/preprocessed_conflict_owner_sample.png",
            doc_type="Pattadar/Land Ownership Record",
            language="English",
            format_type="Printed",
            status="Owner Conflict",
            confidence_score=87.5,
            ocr_text="""
            Government of Andhra Pradesh - Land Records Department
            Pattadar Passbook - Record of Rights
            District: West Godavari
            Mandal: Pedapadu
            Village: Krishnapuram
            Survey Number: 145/3A
            Khata Number: 412
            Plot Number: 12
            Area: 2.50 Acres
            Owner Name: Bandi Ramesh
            Land Classification: Dry - Agricultural
            Ownership Type: Pattadar
            Registration Number: 9912/2023
            """,
            created_at=datetime.datetime.utcnow() - datetime.timedelta(days=2)
        )
        db.add(doc3)
        db.flush()

        rec3 = LandRecord(
            document_id=doc3.id,
            owner_name="Bandi Ramesh",
            survey_number="145/3A",
            khasra_number=None,
            khata_number="412",
            plot_number="12",
            area=2.50,
            area_unit="Acres",
            village="Krishnapuram",
            tehsil_mandal="Pedapadu",
            district="West Godavari",
            land_classification="Dry - Agricultural",
            ownership_type="Pattadar",
            registration_number="9912/2023",
            confidence_scores={
                "owner_name": 88.0, "survey_number": 90.0, "area": 92.0,
                "village": 85.0, "tehsil_mandal": 88.0, "district": 85.0
            },
            verification_status="Pending",
            created_at=doc3.created_at,
            updated_at=doc3.created_at
        )
        db.add(rec3)
        db.flush()

        # Add ValidationResult for Owner Conflict
        v_conflict = ValidationResult(
            document_id=doc3.id,
            rule_name="Owner Conflict",
            severity="Error",
            description="Ownership conflict: Document names owner as 'Bandi Ramesh', but database lists 'Kondru Ramu' for Survey 145/3A. A mutation record may be required.",
            is_resolved=False,
            created_at=doc3.created_at
        )
        db.add(v_conflict)

        # 6. Seed Document 4: Area Mismatch Record (Status: Area Mismatch)
        doc4 = Document(
            original_filename="area_mismatch_sample.png",
            file_path="uploads/area_mismatch_sample.png",
            preprocessed_path="/static/preprocessed/preprocessed_area_mismatch_sample.png",
            doc_type="Survey Record",
            language="English",
            format_type="Printed",
            status="Area Mismatch",
            confidence_score=91.0,
            ocr_text="""
            SURVEY BOUNDARY MEASUREMENT SHEET (FMB)
            Office of the Deputy Surveyor - Pedapadu
            District: West Godavari
            Village: Krishnapuram
            Survey Number: 145/3A
            Total Measured Area: 3.10 Acres
            Owner Name: Kondru Ramu
            """,
            created_at=datetime.datetime.utcnow() - datetime.timedelta(days=1)
        )
        db.add(doc4)
        db.flush()

        rec4 = LandRecord(
            document_id=doc4.id,
            owner_name="Kondru Ramu",
            survey_number="145/3A",
            khasra_number=None,
            khata_number=None,
            plot_number=None,
            area=3.10,
            area_unit="Acres",
            village="Krishnapuram",
            tehsil_mandal="Pedapadu",
            district="West Godavari",
            land_classification=None,
            ownership_type=None,
            confidence_scores={
                "owner_name": 95.0, "survey_number": 95.0, "area": 95.0,
                "village": 95.0, "tehsil_mandal": 95.0, "district": 95.0
            },
            verification_status="Pending",
            created_at=doc4.created_at,
            updated_at=doc4.created_at
        )
        db.add(rec4)
        db.flush()

        # Add ValidationResult for Area Mismatch
        v_mismatch = ValidationResult(
            document_id=doc4.id,
            rule_name="Area Mismatch",
            severity="Error",
            description="Area mismatch detected: This document lists 3.1 Acres, but existing record (ID: 1) lists 2.5 Acres for Survey 145/3A.",
            is_resolved=False,
            created_at=doc4.created_at
        )
        db.add(v_mismatch)

        # 7. Seed Document 5: Telugu Handwritten Record (Status: Low Confidence)
        doc5 = Document(
            original_filename="Telugu_Handwritten_Register.png",
            file_path="uploads/Telugu_Handwritten_Register.png",
            preprocessed_path="/static/preprocessed/preprocessed_Telugu_Handwritten_Register.png",
            doc_type="Pattadar/Land Ownership Record",
            language="Telugu",
            format_type="Handwritten",
            status="Low Confidence",
            confidence_score=52.8,
            ocr_text="""
            ఆంధ్రప్రదేశ్ ప్రభుత్వం
            హస్తలిఖిత రికార్డు - పహాని
            గ్రామం: కృష్ణపురం
            మండలం: పెదపాడు
            జిల్లా: పశ్చిమ గోదావరి
            భూ యజమాని: కాండ్రు రాము
            సర్వే నెం: 145/3A
            విస్తీర్ణం: 2.50
            (మసకగా ఉన్న పాఠ్యం - OCR స్పష్టత తక్కువగా ఉంది)
            """,
            created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=4)
        )
        db.add(doc5)
        db.flush()

        rec5 = LandRecord(
            document_id=doc5.id,
            owner_name="Kondru Ramu",  # Corrected spelling mapping from కాండ్రు రాము
            survey_number="145/3A",
            khasra_number=None,
            khata_number=None,
            plot_number=None,
            area=2.50,
            area_unit="Acres",
            village="Krishnapuram",
            tehsil_mandal="Pedapadu",
            district="West Godavari",
            land_classification=None,
            ownership_type=None,
            confidence_scores={
                "owner_name": 45.0, "survey_number": 60.0, "area": 55.0,
                "village": 80.0, "tehsil_mandal": 80.0, "district": 80.0
            },
            verification_status="Pending",
            regional_values={
                "owner_name": "కాండ్రు రాము",
                "village": "కృష్ణపురం",
                "tehsil_mandal": "పెదపాడు",
                "district": "పశ్చిమ గోదావరి"
            },
            created_at=doc5.created_at,
            updated_at=doc5.created_at
        )
        db.add(rec5)
        db.flush()

        # Add ValidationResult for Low Confidence
        v_low_conf = ValidationResult(
            document_id=doc5.id,
            rule_name="Format Error",
            severity="Warning",
            description="Low recognition confidence: Text read with confidence score 52.8%. Human verification is required.",
            is_resolved=False,
            created_at=doc5.created_at
        )
        db.add(v_low_conf)

        # 8. Seed Document 6: Mutation Record (Status: Pending Review)
        doc6 = Document(
            original_filename="mutation_record_sample.png",
            file_path="uploads/mutation_record_sample.png",
            preprocessed_path="/static/preprocessed/preprocessed_mutation_record_sample.png",
            doc_type="Mutation Record",
            language="English",
            format_type="Printed",
            status="Pending Review",
            confidence_score=94.2,
            ocr_text="""
            LAND REVENUE DEPARTMENT - MUTATION REGISTER
            FORM VIII (Mutation Order)
            Mandal: Pedapadu
            Village: Krishnapuram
            Mutation Number: MUT/2025/892
            Survey Number: 145/3A
            Khata Number: 412
            Area Affected: 2.50 Acres
            Original Owner (Transferor): Kondru Ramu
            New Owner (Transferee): Kondru Suresh
            Ownership Type: Pattadar
            Reason for Mutation: Sale Deed Registry
            Registration Number: 4821/2025
            Registration Date: 15-08-2025
            Order Date: 20-08-2025
            """,
            created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=2)
        )
        db.add(doc6)
        db.flush()

        rec6 = LandRecord(
            document_id=doc6.id,
            owner_name="Kondru Suresh",  # Transferring to Suresh
            survey_number="145/3A",
            khasra_number=None,
            khata_number="412",
            plot_number=None,
            area=2.50,
            area_unit="Acres",
            village="Krishnapuram",
            tehsil_mandal="Pedapadu",
            district="West Godavari",
            land_classification="Dry - Agricultural",
            ownership_type="Pattadar",
            mutation_number="MUT/2025/892",
            registration_number="4821/2025",
            registration_date="15-08-2025",
            confidence_scores={
                "owner_name": 95.0, "survey_number": 95.0, "area": 95.0,
                "village": 95.0, "tehsil_mandal": 95.0, "district": 95.0,
                "mutation_number": 95.0, "registration_number": 95.0
            },
            verification_status="Pending",
            created_at=doc6.created_at,
            updated_at=doc6.created_at
        )
        db.add(rec6)
        db.flush()

        # 9. Seed Document 7: Hindi Khasra (Verified, translated to English)
        doc7 = Document(
            original_filename="hindi_khasra_sample.png",
            file_path="uploads/hindi_khasra_sample.png",
            preprocessed_path="/static/preprocessed/preprocessed_hindi_khasra_sample.png",
            doc_type="Pattadar/Land Ownership Record",
            language="Hindi",
            format_type="Printed",
            status="Verified",
            confidence_score=94.5,
            ocr_text="""
उत्तर प्रदेश सरकार - भू-राजस्व विभाग
अधिकार अभिलेख (खाता खतौनी)
ग्राम: रामपुर (Rampur)
तहसील: हापुड़ (Hapur)
जनपद: मेरठ (Meerut)
खाता संख्या (Khata Number): 882
खसरा संख्या (Khasra Number): 145/3A
स्वामित्व प्रकार (Ownership): खुदकाश्त (Self-Cultivated)
खातेदार का नाम (Owner Name): रामेश सिंह (Ramesh Singh)
पिता का नाम: हरि सिंह
क्षेत्रफल (Area): 2.50 एकड़ (Acres)
भूमि वर्गीकरण (Classification): कृषि भूमि (Agricultural Land)
पंजीकरण संख्या (Registration Number): 4012/2024
पंजीकरण दिनांक (Registration Date): 12-04-2024
            """,
            created_at=datetime.datetime.utcnow() - datetime.timedelta(days=4)
        )
        db.add(doc7)
        db.flush()

        rec7 = LandRecord(
            document_id=doc7.id,
            owner_name="Ramesh Singh",
            survey_number="145/3A",
            khasra_number="145/3A",
            khata_number="882",
            area=2.50,
            area_unit="Acres",
            village="Rampur",
            tehsil_mandal="Hapur",
            district="Meerut",
            land_classification="Agricultural Land",
            ownership_type="Self-Cultivated",
            registration_number="4012/2024",
            registration_date="12-04-2024",
            confidence_scores={
                "owner_name": 95.0, "survey_number": 95.0, "area": 95.0,
                "village": 95.0, "tehsil_mandal": 95.0, "district": 95.0
            },
            verification_status="Verified",
            regional_values={
                "owner_name": "रामेश सिंह",
                "village": "रामपुर",
                "tehsil_mandal": "हापुड़",
                "district": "मेरठ",
                "land_classification": "कृषि भूमि",
                "ownership_type": "खुदकाश्त"
            },
            created_at=doc7.created_at,
            updated_at=doc7.created_at
        )
        db.add(rec7)
        db.flush()

        # 10. Seed Document 8: Tamil Patta (Verified, translated to English)
        doc8 = Document(
            original_filename="tamil_patta_sample.jpg",
            file_path="uploads/tamil_patta_sample.jpg",
            preprocessed_path="/static/preprocessed/preprocessed_tamil_patta_sample.png",
            doc_type="Pattadar/Land Ownership Record",
            language="Tamil",
            format_type="Printed",
            status="Verified",
            confidence_score=92.8,
            ocr_text="""
தமிழ்நாடு அரசு - வருவாய்த் துறை
பட்டா உரிமை நகல்
மாவட்டம்: மதுரை (Madurai)
வட்டம்: சோழவந்தான் (Sholavandan)
கிராமம்: சோழவந்தான் (Sholavandan)
பட்டா எண்: 412
உரிமையாளர் பெயர்: கிருஷ்ணமூர்த்தி (Krishnamurthy)
புல எண்: 145/3A
பரப்பளவு: 2.50 ஹெக்டேர் (Hectares)
நில வகைப்பாடு: நஞ்சை (Wet Land)
பதிவு எண்: 9122/2023
பதிவு தேதி: 10-09-2023
            """,
            created_at=datetime.datetime.utcnow() - datetime.timedelta(days=3)
        )
        db.add(doc8)
        db.flush()

        rec8 = LandRecord(
            document_id=doc8.id,
            owner_name="Krishnamurthy",
            survey_number="145/3A",
            khata_number="412",
            area=2.50,
            area_unit="Hectares",
            village="Sholavandan",
            tehsil_mandal="Sholavandan",
            district="Madurai",
            land_classification="Wet Land",
            ownership_type="Patta",
            registration_number="9122/2023",
            registration_date="10-09-2023",
            confidence_scores={
                "owner_name": 93.0, "survey_number": 95.0, "area": 92.0,
                "village": 93.0, "tehsil_mandal": 92.0, "district": 94.0
            },
            verification_status="Verified",
            regional_values={
                "owner_name": "கிருஷ்ணமூர்த்தி",
                "village": "சோழவந்தான்",
                "tehsil_mandal": "சோழவந்தான்",
                "district": "மதுரை",
                "land_classification": "நஞ்சை",
                "ownership_type": "பட்டா"
            },
            created_at=doc8.created_at,
            updated_at=doc8.created_at
        )
        db.add(rec8)
        db.flush()

        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
