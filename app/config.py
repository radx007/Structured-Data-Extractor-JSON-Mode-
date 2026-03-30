class Settings:

    APP_NAME = "Vehicle Document AI"

    OCR_LANG = "en"

    MAX_UPLOAD_FILES = 4
    
    MAX_SIZE = 5 * 1024 * 1024  # 5MB

    _packing_list = {
                    "type_document": "packing_list",
                    "donnees_extraites": {
                        "destinataire": "string",
                        "passport": "string",
                        "numero_s_c": "string",
                        "numero_facture": "string",
                        "numero_packing_list": "string",
                        "date": "date",
                        "expediteur": "string",
                        "lieu_depart": "string",
                        "lieu_arrivee": "string",
                        "pays_origine": "string",
                        "items": [
                        {
                            "marques": "string",
                            "description": "string",
                            "vin": "string",
                            "quantite": "number",
                            "poids_net_kg": "number",
                            "poids_brut_kg": "number",
                            "volume_m3": "number"
                        }
                        ],
                        "totaux": {
                        "quantite": "number",
                        "poids_net_kg": "number",
                        "poids_brut_kg": "number",
                        "volume_m3": "number"
                        }
                    }
                    }
    _certificate_of_origin = {
                            "type_document": "certificate_of_origin",
                            "donnees_extraites": {
                                "numero_certificat": "string",
                                "verification": "string",
                                "exportateur": {
                                "nom": "string",
                                "adresse": "string",
                                "pays": "string"
                                },
                                "destinataire": {
                                "nom": "string",
                                "passport": "string",
                                "nin": "string",
                                "email": "string",
                                "telephone": "string",
                                "adresse": "string",
                                "pays": "string"
                                },
                                "transport": {
                                "mode": "string",
                                "port_depart": "string",
                                "port_arrivee": "string",
                                "pays_depart": "string",
                                "pays_arrivee": "string"
                                },
                                "pays_destination": "string",
                                "marchandises": [
                                {
                                    "marques": "string",
                                    "description": "string",
                                    "vin": "string",
                                    "modele": "string",
                                    "annee_fabrication": "number",
                                    "fabricant": "string",
                                    "poids_unitaire_kg": "number",
                                    "quantite": "number"
                                }
                                ],
                                "classification": {
                                "hs_code": "string"
                                },
                                "facture": {
                                "numero_facture": "string",
                                "date_facture": "date"
                                }
                            }
                            }
    _invoice = {
                "type_document": "invoice",
                "donnees_extraites": {
                    "exportateur": {
                    "nom": "string",
                    "adresse": "string",
                    "pays": "string"
                    },
                    "destinataire": {
                    "nom": "string",
                    "passport": "string"
                    },
                    "numero_s_c": "string",
                    "numero_facture": "string",
                    "date_facture": "date",
                    "termes_commerciaux": "string",
                    "transport": {
                    "lieu_depart": "string",
                    "lieu_arrivee": "string",
                    "pays_depart": "string",
                    "pays_arrivee": "string"
                    },
                    "origine": {
                    "pays_origine": "string",
                    "hs_code": "string"
                    },
                    "marchandises": [
                    {
                        "marques": "string",
                        "description": "string",
                        "vin": "string",
                        "quantite": "number",
                        "prix_unitaire": "number",
                        "montant": "number",
                        "devise": "string"
                    }
                    ],
                    "frais": {
                    "fret_maritime": "number",
                    "autres_frais": "number"
                    },
                    "totaux": {
                    "quantite_totale": "number",
                    "montant_total": "number",
                    "devise": "string",
                    "montant_total_lettres": "string"
                    }
                }
                }
    _technical_details = {
                        "type_document": "technical_details",
                        "donnees_extraites": {
                            "numero_certificat": "string",
                            "date_emission": "date",
                            "fabricant": "string",
                            "marque": "string",
                            "nom_vehicule": "string",
                            "modele": "string",
                            "numero_chassis": "string",
                            "numero_moteur": "string",
                            "date_fabrication": "date",
                            "poids_vehicule_kg": {
                            "poids_total": "number",
                            "poids_a_vide": "number",
                            "charge_utile": "number"
                            },
                            "capacite": {
                            "nombre_places": "number",
                            "capacite_passagers": "number"
                            },
                            "performance": {
                            "vitesse_max_kmh": "number",
                            "puissance_moteur_kw": "number"
                            },
                            "remorquage": {
                            "capacite_remorquage_max_kg": "number",
                            "poids_remorque_autorise_kg": "number"
                            },
                            "equipements": {
                            "abs_modele": "string",
                            "abs_fabricant": "string",
                            "options": "string",
                            "systeme_edr": "boolean"
                            },
                            "conformite": {
                            "norme": "string",
                            "organisme_certification": "string"
                            },
                            "qr_code": "string",
                            "remarques": "string"
                        }
                        }

    schemas = {
        "packing_list": _packing_list,
        "certificate_of_origin": _certificate_of_origin,
        "invoice": _invoice,
        "technical_details": _technical_details
    }

    instructions = {
        "packing_list": (
            "PRIMARY TASK: Extract all header and footer data. "
            "1. DESTINATAIRE: You MUST extract the 'Name' and 'Identity' (Passport/NIN). Strip 'Passport:' prefix; return ONLY the 9+ digit number. "
            "2. TRANSPORT: Map 'lieu_depart' as the Origin Port (Loading) and 'lieu_arrivee' as the Destination Port (Skikda). "
            "3. DATE: Convert any date format found to 'YYYY-MM-DD'. "
            "4. ITEMS ARRAY: For each row, map 'vin' (17 chars), 'description' (Brand + Model only), and 'marques' (Literal 'N/M'). "
            "   - Remove 'VIN CODE:' from the description. "
            "   - Convert weights/volumes to clean Floats and 'quantite' to Integer. "
            "5. TOTAUX: This section is MANDATORY. Extract the final sums of Qty, Weight, and Volume from the document footer. "
            "   - If the footer is unreadable, you MUST sum the item rows manually to populate these fields. "
            "6. FINAL RULE: Do not return 'None' for fields present in the text. Set missing data to null."
        ),
        "certificate_of_origin": (
            "Map the OCR text to the schema by identifying the 'numero_certificat' (unique document ID) and the 'verification' URL or authority code. "
            "In 'donnees_extraites.destinataire', parse the identity block for 'nom', 'passport', 18-digit 'nin', 'email', and 'telephone'—extract values following these specific labels. "
            "For 'transport', dynamically map the 'FROM' location to 'port_depart' and 'TO' location to 'port_arrivee', identifying countries of origin and destination from the text. "
            "In the 'marchandises' array, isolate the 17-character 'vin', the alphanumeric 'modele', and 'annee_fabrication' from the technical description block. "
            "In 'marchandises', extract the Commercial Name (Brand + Model name, e.g., 'MG5') into 'description'. "
            "Map 'hs_code' from the classification column and link 'numero_facture' and 'date_facture' (normalized to YYYY-MM-DD) from the invoice reference section. "
            "Assign 'N/M' literally to 'marques' if present; set truly missing fields to null without hallucinating data."
            "FINAL RULE: Do not return 'None' for fields present in the text. Set missing data to null."
        ),
        "commercial_invoice": (
            "PRIMARY TASK: Perform a Financial Audit and extraction of all trade terms. "
            "1. HEADER: Identify 'numero_facture' and 'date_facture'. MANDATORY: Normalize date to 'YYYY-MM-DD'. "
            "2. ENTITIES: Extract 'vendeur' (Exporter) and 'acheteur' (Importer Name + Identity). Clean 'Identity' to raw numbers only. "
            "3. TRADE LOGIC: Identify 'incoterm' (FOB, CFR, CIF, etc.) and map 'port_chargement' (Origin) vs 'port_dechargement' (Destination). "
            "4. ITEMS ARRAY: For every vehicle, extract 'vin' (17 chars), 'description' (Brand + Model only), 'quantite' (Integer), 'prix_unitaire' (Float), and 'montant_ligne' (Qty * Unit Price). "
            "5. ADDITIONAL COSTS: Identify 'frais_fret' (Freight) and 'frais_assurance' (Insurance) if listed separately. "
            "6. FINANCIAL TOTALS: "
            "   - Extract 'montant_total_lettres' (The full Grand Total written in WORDS). "
            "   - Extract 'montant_total' (The Grand Total in NUMBERS). "
            "   - DEVISE: Identify the ISO currency code (USD, EUR). "
            "7. VERIFICATION RULE: The 'montant_global_chiffres' MUST reflect the sum of all item amounts + additional costs. If they differ, flag in a 'notes' field. "
            "8. SANITIZATION: Strip all symbols ($, €) and unit labels (USD) from numbers. Return null only if data is truly absent."
            "FINAL RULE: Do not return 'None' for fields present in the text. Set missing data to null."
        ),
        "technical_details": (
            "PRIMARY TASK: High-Precision Engineering & Compliance Extraction. "
            "1. IDENTITIES: Extract 'numero_chassis' (17-char VIN) and 'numero_moteur' (Engine Serial). "
            "   CRITICAL: These must be extracted exactly as printed, preserving capitalization. "
            "2. CHRONOLOGY: Identify 'date_emission' (Certificate Date) and 'date_fabrication' (Production Date). "
            "   RULE: Strictly normalize all dates to 'YYYY-MM-DD'. "
            "3. ENTITIES: Map 'fabricant' (Manufacturer Name), 'marque' (Brand, e.g., MG), and 'modele' (Technical Code). "
            "4. WEIGHT LOGIC (METRIC): "
            "   - Extract 'poids_total' (GVWR) and 'poids_a_vide' (Curb Weight). "
            "   - CALCULATED FIELD: Set 'charge_utile' (Payload) as (poids_total - poids_a_vide). "
            "   - Ensure all values are clean Integers/Numbers (strip 'KG'). "
            "5. CAPACITIES & PERFORMANCE: "
            "   - Extract 'nombre_places' and 'capacite_passagers'. "
            "   - Map 'vitesse_max_kmh' and 'puissance_moteur_kw' (Clean numbers only). "
            "6. EQUIPMENT & SAFETY: "
            "   - Identify 'abs_modele' and 'abs_fabricant'. "
            "   - BOOLEAN LOGIC: Set 'systeme_edr' to true ONLY if the text explicitly mentions 'Event Data Recording' or 'EDR'. "
            "7. COMPLIANCE: Identify the 'norme' (e.g., China VI, Euro 6) and the 'organisme_certification'. "
            "8. REMARKS: Capture any optional equipment (Sunroof, etc.) in the 'remarques' field. "
            "9. SANITIZATION: Missing numeric fields must be null. Strip all units (KW, KM/H, KG). "
            "FINAL RULE: This is a legal compliance document. Do not hallucinate data. If a field is missing, return null."
        ),
        "unknown": "Perform a general extraction of all visible entities into a flat JSON structure."
    }


settings = Settings()