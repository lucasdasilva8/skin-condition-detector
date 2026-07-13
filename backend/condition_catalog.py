"""Canonical skin condition metadata for the PacificRM 22-class model."""

HIGH_RISK_CODES = frozenset(
    {
        "skin_cancer",
        "actinic_keratosis",
        "lupus",
        "vasculitis",
    }
)

LEGACY_CODE_MAP = {
    "akiec": "actinic_keratosis",
    "bcc": "skin_cancer",
    "bkl": "seborrheic_keratoses",
    "df": "benign_tumors",
    "mel": "skin_cancer",
    "nv": "moles",
    "vasc": "vascular_tumors",
}

CONDITIONS = {
    "acne": {
        "name": "Acne",
        "short_name": "Acne",
        "risk_level": "low",
        "description": "A common inflammatory skin condition involving clogged pores, pimples, and sometimes deeper cysts.",
        "explanation": (
            "Acne develops when hair follicles become blocked with oil and dead skin cells, "
            "allowing bacteria to grow and causing inflammation. Hormonal changes, stress, and "
            "certain medications can trigger or worsen breakouts. It most often affects the face, "
            "chest, and back during adolescence but can persist or appear in adulthood."
        ),
        "common_signs": [
            "Whiteheads and blackheads",
            "Red, inflamed pimples or papules",
            "Painful nodules or cysts",
            "Oily skin in affected areas",
            "Post-inflammatory dark spots or scarring",
        ],
        "what_it_means": (
            "Acne is very common and usually not dangerous, though it can affect self-esteem and "
            "leave scars if severe or picked at."
        ),
        "when_to_see_doctor": (
            "See a dermatologist if over-the-counter care does not help after several weeks, "
            "if you have painful cysts or scarring, or if acne is affecting your quality of life."
        ),
        "recommended_actions": [
            {
                "action": "Wash affected areas gently twice daily with a mild cleanser; avoid scrubbing or harsh products.",
                "source": {
                    "title": "Acne: Diagnosis and treatment",
                    "url": "https://www.aad.org/public/diseases/acne/derm-treat/treat",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Use non-comedogenic, oil-free moisturizers and broad-spectrum sunscreen SPF 30 or higher daily.",
                "source": {
                    "title": "Acne",
                    "url": "https://www.mayoclinic.org/diseases-conditions/acne/symptoms-causes/syc-20368047",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Avoid picking or squeezing lesions, which can worsen inflammation and increase scarring risk.",
                "source": {
                    "title": "Acne",
                    "url": "https://www.health.harvard.edu/diseases-and-conditions/acne-a-to-z",
                    "publisher": "Harvard Health Publishing",
                    "domain": "health.harvard.edu",
                },
            },
        ],
        "sources": [
            {
                "title": "Acne",
                "url": "https://www.aad.org/public/diseases/acne",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Acne",
                "url": "https://www.mayoclinic.org/diseases-conditions/acne/symptoms-causes/syc-20368047",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Acne",
                "url": "https://dermnetnz.org/topics/acne",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
    "actinic_keratosis": {
        "name": "Actinic Keratosis",
        "short_name": "Actinic Keratosis",
        "risk_level": "high",
        "description": "Rough, scaly patches caused by long-term sun exposure that may progress to skin cancer.",
        "explanation": (
            "Actinic keratoses (AKs) are precancerous lesions that form on sun-exposed skin after "
            "years of ultraviolet damage. They often feel like dry, sandpaper-like spots that do not "
            "heal. Because a small percentage can develop into squamous cell carcinoma, AKs should "
            "be evaluated and treated by a dermatologist."
        ),
        "common_signs": [
            "Rough, scaly or crusty patches",
            "Pink, red, or flesh-colored flat or raised spots",
            "Lesions on sun-exposed areas (face, scalp, ears, hands)",
            "Spots that persist and do not go away",
            "Mild itching or tenderness",
        ],
        "what_it_means": (
            "Actinic keratosis is a warning sign of significant sun damage and carries a higher "
            "risk of progressing to skin cancer if left untreated."
        ),
        "when_to_see_doctor": (
            "See a dermatologist promptly for any new or changing rough, scaly spot, especially "
            "if you have a history of extensive sun exposure."
        ),
        "recommended_actions": [
            {
                "action": "Apply broad-spectrum sunscreen SPF 30 or higher daily to all exposed skin and reapply every two hours outdoors.",
                "source": {
                    "title": "Actinic keratosis",
                    "url": "https://www.skincancer.org/risk-factors/actinic-keratosis/",
                    "publisher": "Skin Cancer Foundation",
                    "domain": "skincancer.org",
                },
            },
            {
                "action": "Wear protective clothing, wide-brimmed hats, and seek shade during peak sun hours.",
                "source": {
                    "title": "Actinic keratosis",
                    "url": "https://www.aad.org/public/diseases/skin-cancer/actinic-keratosis-what-is",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Schedule a full skin examination with a dermatologist for diagnosis and treatment options.",
                "source": {
                    "title": "Actinic keratosis",
                    "url": "https://www.mayoclinic.org/diseases-conditions/actinic-keratosis/symptoms-causes/syc-20372385",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Actinic keratosis",
                "url": "https://www.aad.org/public/diseases/skin-cancer/actinic-keratosis-what-is",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Actinic keratosis",
                "url": "https://www.skincancer.org/risk-factors/actinic-keratosis/",
                "publisher": "Skin Cancer Foundation",
                "domain": "skincancer.org",
            },
            {
                "title": "Actinic keratosis",
                "url": "https://dermnetnz.org/topics/actinic-keratosis",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
    "benign_tumors": {
        "name": "Benign Skin Tumor",
        "short_name": "Benign Tumor",
        "risk_level": "low",
        "description": "Non-cancerous growths such as dermatofibromas that are usually harmless but may resemble other lesions.",
        "explanation": (
            "Benign skin tumors include growths like dermatofibromas, lipomas, and other non-malignant "
            "nodules. They typically grow slowly, stay stable in size, and do not spread to other parts "
            "of the body. Because they can look similar to more concerning lesions, a professional "
            "examination helps confirm the diagnosis."
        ),
        "common_signs": [
            "Firm, raised nodule on the skin",
            "Brown, pink, or flesh-colored appearance",
            "Dimpling when pinched (dermatofibroma sign)",
            "Slow growth or no change over time",
            "Usually painless unless irritated",
        ],
        "what_it_means": (
            "Benign tumors are generally not dangerous and often require no treatment unless they "
            "cause discomfort or cosmetic concern."
        ),
        "when_to_see_doctor": (
            "See a dermatologist if a growth is new, changing, painful, bleeding, or you are unsure "
            "whether it is benign."
        ),
        "recommended_actions": [
            {
                "action": "Monitor the lesion for changes in size, color, shape, or symptoms and note any changes with photos.",
                "source": {
                    "title": "How to spot skin cancer",
                    "url": "https://www.aad.org/public/diseases/skin-cancer/find/at-risk/spot-skin-cancer",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Avoid traumatizing or repeatedly rubbing the area, which can cause irritation.",
                "source": {
                    "title": "Dermatofibroma",
                    "url": "https://dermnetnz.org/topics/dermatofibroma",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
            {
                "action": "Have a dermatologist evaluate any uncertain growth to confirm it is benign.",
                "source": {
                    "title": "Skin cancer",
                    "url": "https://www.mayoclinic.org/diseases-conditions/skin-cancer/symptoms-causes/syc-20377605",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Dermatofibroma",
                "url": "https://dermnetnz.org/topics/dermatofibroma",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
            {
                "title": "Skin cancer",
                "url": "https://www.aad.org/public/diseases/skin-cancer",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Skin cancer",
                "url": "https://www.mayoclinic.org/diseases-conditions/skin-cancer/symptoms-causes/syc-20377605",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
        ],
    },
    "bullous": {
        "name": "Bullous Disease",
        "short_name": "Bullous",
        "risk_level": "moderate",
        "description": "Blistering skin conditions where fluid-filled bubbles form in or on the skin.",
        "explanation": (
            "Bullous diseases encompass a group of disorders that cause blisters, ranging from "
            "autoimmune conditions like pemphigus and bullous pemphigoid to drug reactions and "
            "infections. The blisters form when layers of skin separate and fill with fluid. "
            "Because some bullous diseases can be serious, prompt medical evaluation is important."
        ),
        "common_signs": [
            "Fluid-filled blisters (bullae) on skin or mucous membranes",
            "Itching, burning, or pain around blisters",
            "Crusting or erosions after blisters rupture",
            "Widespread or localized distribution",
            "Mouth or eye involvement in some cases",
        ],
        "what_it_means": (
            "Bullous skin findings can signal an autoimmune disorder, infection, or reaction that "
            "may need targeted medical treatment."
        ),
        "when_to_see_doctor": (
            "Seek medical care promptly for new or widespread blisters, blisters with fever, "
            "mouth or eye involvement, or if blisters are spreading rapidly."
        ),
        "recommended_actions": [
            {
                "action": "Do not intentionally pop blisters; keep affected skin clean and covered with a loose, sterile dressing if needed.",
                "source": {
                    "title": "Blisters: First aid",
                    "url": "https://www.mayoclinic.org/first-aid/first-aid-blisters/basics/art-20056691",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Avoid known triggers such as certain medications until evaluated by a physician.",
                "source": {
                    "title": "Bullous pemphigoid",
                    "url": "https://dermnetnz.org/topics/bullous-pemphigoid",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
            {
                "action": "See a dermatologist for diagnosis, which may require a skin biopsy and blood tests.",
                "source": {
                    "title": "Pemphigus",
                    "url": "https://www.aad.org/public/diseases/a-z/pemphigus-overview",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Bullous pemphigoid",
                "url": "https://dermnetnz.org/topics/bullous-pemphigoid",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
            {
                "title": "Pemphigus",
                "url": "https://www.aad.org/public/diseases/a-z/pemphigus-overview",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Bullous pemphigoid",
                "url": "https://www.mayoclinic.org/diseases-conditions/bullous-pemphigoid/symptoms-causes/syc-20350404",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
        ],
    },
    "candidiasis": {
        "name": "Candidiasis",
        "short_name": "Candidiasis",
        "risk_level": "low",
        "description": "A fungal yeast infection of the skin or mucous membranes causing redness and irritation.",
        "explanation": (
            "Cutaneous candidiasis is caused by overgrowth of Candida yeast, often in warm, moist "
            "areas like skin folds, the groin, or under the breasts. It thrives when skin stays damp "
            "or when the normal balance of microorganisms is disrupted. People with diabetes, weakened "
            "immunity, or antibiotic use are at higher risk."
        ),
        "common_signs": [
            "Bright red rash with scalloped borders",
            "Satellite pustules or small red spots nearby",
            "Itching and burning sensation",
            "Moist, macerated skin in folds",
            "White patches in mouth (oral thrush)",
        ],
        "what_it_means": (
            "Candidiasis is usually treatable with antifungal care, though it may recur if underlying "
            "moisture or health conditions are not addressed."
        ),
        "when_to_see_doctor": (
            "See a doctor if the rash does not improve with keeping the area dry, if you have "
            "diabetes or a weakened immune system, or if the infection spreads."
        ),
        "recommended_actions": [
            {
                "action": "Keep affected skin clean and dry; pat dry thoroughly after bathing and change damp clothing promptly.",
                "source": {
                    "title": "Candidiasis",
                    "url": "https://dermnetnz.org/topics/candida-infection-of-the-skin",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
            {
                "action": "Wear loose, breathable cotton clothing and avoid occlusive fabrics in affected areas.",
                "source": {
                    "title": "Yeast infection (vaginal)",
                    "url": "https://www.mayoclinic.org/diseases-conditions/yeast-infection/symptoms-causes/syc-20378999",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Consult a healthcare provider for appropriate antifungal treatment if symptoms persist.",
                "source": {
                    "title": "Candidiasis",
                    "url": "https://www.aad.org/public/diseases/a-z/candidiasis",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Candida infection of the skin",
                "url": "https://dermnetnz.org/topics/candida-infection-of-the-skin",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
            {
                "title": "Candidiasis",
                "url": "https://www.aad.org/public/diseases/a-z/candidiasis",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Yeast infection (vaginal)",
                "url": "https://www.mayoclinic.org/diseases-conditions/yeast-infection/symptoms-causes/syc-20378999",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
        ],
    },
    "drug_eruption": {
        "name": "Drug Eruption",
        "short_name": "Drug Reaction",
        "risk_level": "moderate",
        "description": "A skin rash or reaction triggered by a medication or drug exposure.",
        "explanation": (
            "Drug eruptions occur when the immune system reacts to a medication, producing rashes "
            "that can range from mild hives to severe, life-threatening reactions. Common triggers "
            "include antibiotics, anti-seizure drugs, and nonsteroidal anti-inflammatory medications. "
            "Identifying and stopping the causative drug is the most important step."
        ),
        "common_signs": [
            "New rash appearing days to weeks after starting a medication",
            "Red, itchy patches or hives",
            "Morbilliform (measles-like) eruption",
            "Fever accompanying the rash in some cases",
            "Blistering or skin peeling in severe reactions",
        ],
        "what_it_means": (
            "A drug-related rash signals your body is reacting to a medication and may require "
            "stopping the drug and medical evaluation."
        ),
        "when_to_see_doctor": (
            "Seek urgent care for rash with fever, facial swelling, difficulty breathing, or "
            "widespread blistering; otherwise contact your doctor promptly about any new rash after starting a drug."
        ),
        "recommended_actions": [
            {
                "action": "Contact your prescribing physician immediately about any new rash after starting a medication; do not stop prescribed drugs without medical guidance.",
                "source": {
                    "title": "Drug rash",
                    "url": "https://dermnetnz.org/topics/drug-eruptions",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
            {
                "action": "Take note of all medications, supplements, and when symptoms started to share with your healthcare provider.",
                "source": {
                    "title": "Drug allergy",
                    "url": "https://www.mayoclinic.org/diseases-conditions/drug-allergy/symptoms-causes/syc-20371801",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Use cool compresses and gentle moisturizing for mild itching while awaiting medical advice.",
                "source": {
                    "title": "Drug rashes",
                    "url": "https://www.aad.org/public/diseases/a-z/drug-rashes",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Drug eruptions",
                "url": "https://dermnetnz.org/topics/drug-eruptions",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
            {
                "title": "Drug allergy",
                "url": "https://www.mayoclinic.org/diseases-conditions/drug-allergy/symptoms-causes/syc-20371801",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Drug rashes",
                "url": "https://www.aad.org/public/diseases/a-z/drug-rashes",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
        ],
    },
    "eczema": {
        "name": "Eczema (Atopic Dermatitis)",
        "short_name": "Eczema",
        "risk_level": "moderate",
        "description": "A chronic inflammatory skin condition causing dry, itchy, inflamed patches.",
        "explanation": (
            "Eczema, also called atopic dermatitis, results from a combination of genetic factors, "
            "immune dysregulation, and environmental triggers that weaken the skin barrier. Flare-ups "
            "can be triggered by dry air, irritants, allergens, stress, and infections. It often "
            "begins in childhood but can affect people of all ages."
        ),
        "common_signs": [
            "Dry, scaly, or cracked skin",
            "Intense itching, especially at night",
            "Red or brownish-gray patches",
            "Small raised bumps that may leak fluid",
            "Thickened, leathery skin from chronic scratching",
        ],
        "what_it_means": (
            "Eczema is a manageable chronic condition, though flare-ups can significantly affect "
            "comfort and sleep if not treated."
        ),
        "when_to_see_doctor": (
            "See a dermatologist if eczema is not controlled with basic moisturizing, if skin "
            "becomes infected (oozing, crusting, fever), or if it severely affects daily life."
        ),
        "recommended_actions": [
            {
                "action": "Apply fragrance-free moisturizer liberally at least twice daily, especially after bathing.",
                "source": {
                    "title": "Eczema: Tips for managing",
                    "url": "https://www.aad.org/public/diseases/eczema/atopic-dermatitis-AD/treatment/treatment",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Use lukewarm (not hot) baths or showers and pat skin dry gently rather than rubbing.",
                "source": {
                    "title": "Atopic dermatitis (eczema)",
                    "url": "https://www.mayoclinic.org/diseases-conditions/atopic-dermatitis-eczema/symptoms-causes/syc-20353273",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Avoid scratching; keep nails short and consider cool compresses during itchy flare-ups.",
                "source": {
                    "title": "Eczema",
                    "url": "https://www.health.harvard.edu/diseases-and-conditions/eczema-a-to-z",
                    "publisher": "Harvard Health Publishing",
                    "domain": "health.harvard.edu",
                },
            },
        ],
        "sources": [
            {
                "title": "Eczema",
                "url": "https://www.aad.org/public/diseases/eczema",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Atopic dermatitis (eczema)",
                "url": "https://www.mayoclinic.org/diseases-conditions/atopic-dermatitis-eczema/symptoms-causes/syc-20353273",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Atopic dermatitis",
                "url": "https://dermnetnz.org/topics/atopic-dermatitis",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
    "infestations_bites": {
        "name": "Infestations and Bites",
        "short_name": "Bites/Infestations",
        "risk_level": "moderate",
        "description": "Skin reactions from insect bites, stings, or parasitic infestations such as scabies.",
        "explanation": (
            "Infestations and bites cause skin inflammation through direct injury, allergic reactions "
            "to saliva or venom, or parasitic organisms living on or in the skin. Common examples "
            "include mosquito bites, bedbug bites, and scabies mites. Secondary infection can occur "
            "from scratching, and some infestations spread easily to close contacts."
        ),
        "common_signs": [
            "Itchy red bumps or welts",
            "Linear burrows (scabies)",
            "Grouped bite marks in exposed areas",
            "Swelling and warmth at bite site",
            "Signs of infection: pus, increasing pain, red streaks",
        ],
        "what_it_means": (
            "Most bites and infestations are treatable, but some require prescription treatment "
            "and household measures to prevent spread or reinfestation."
        ),
        "when_to_see_doctor": (
            "See a doctor for suspected scabies, signs of infection, severe allergic reactions, "
            "or bites that worsen despite basic care."
        ),
        "recommended_actions": [
            {
                "action": "Clean bite areas with mild soap and water; apply a cool compress to reduce swelling and itching.",
                "source": {
                    "title": "Insect bites and stings: First aid",
                    "url": "https://www.mayoclinic.org/first-aid/first-aid-insect-bites/basics/art-20056593",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Avoid scratching to prevent skin breakdown and secondary bacterial infection.",
                "source": {
                    "title": "Scabies",
                    "url": "https://www.aad.org/public/diseases/a-z/scabies-overview",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Seek medical evaluation for suspected scabies or lice, which require specific prescription treatment for you and close contacts.",
                "source": {
                    "title": "Scabies",
                    "url": "https://dermnetnz.org/topics/scabies",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Scabies",
                "url": "https://www.aad.org/public/diseases/a-z/scabies-overview",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Scabies",
                "url": "https://dermnetnz.org/topics/scabies",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
            {
                "title": "Insect bites and stings",
                "url": "https://www.mayoclinic.org/first-aid/first-aid-insect-bites/basics/art-20056593",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
        ],
    },
    "lichen": {
        "name": "Lichen Planus",
        "short_name": "Lichen",
        "risk_level": "moderate",
        "description": "An inflammatory condition causing itchy, flat-topped purple bumps on the skin or mucous membranes.",
        "explanation": (
            "Lichen planus is thought to be an autoimmune or immune-mediated reaction that affects "
            "the skin, nails, scalp, and mouth. It often presents as polygonal, purple, flat-topped "
            "papules with fine white lines (Wickham striae). While usually not life-threatening, "
            "oral lichen planus requires monitoring because of a small association with oral cancer."
        ),
        "common_signs": [
            "Flat-topped, purple or reddish bumps",
            "Intense itching",
            "White lacy patches in the mouth",
            "Nail ridges or thinning",
            "Scalp involvement with hair loss (lichen planopilaris)",
        ],
        "what_it_means": (
            "Lichen planus is a chronic inflammatory condition that can cause significant discomfort "
            "and may need long-term dermatologic management."
        ),
        "when_to_see_doctor": (
            "See a dermatologist for diagnosis and treatment, especially if mouth, genital, or "
            "scalp areas are involved."
        ),
        "recommended_actions": [
            {
                "action": "Avoid scratching affected areas to reduce the risk of scarring and secondary infection.",
                "source": {
                    "title": "Lichen planus",
                    "url": "https://www.aad.org/public/diseases/a-z/lichen-planus-overview",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Use gentle skin care without harsh soaps or fragrances on affected areas.",
                "source": {
                    "title": "Lichen planus",
                    "url": "https://www.mayoclinic.org/diseases-conditions/lichen-planus/symptoms-causes/syc-20351378",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Schedule regular dental checkups if you have oral lichen planus for ongoing monitoring.",
                "source": {
                    "title": "Lichen planus",
                    "url": "https://dermnetnz.org/topics/lichen-planus",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Lichen planus",
                "url": "https://www.aad.org/public/diseases/a-z/lichen-planus-overview",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Lichen planus",
                "url": "https://www.mayoclinic.org/diseases-conditions/lichen-planus/symptoms-causes/syc-20351378",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Lichen planus",
                "url": "https://dermnetnz.org/topics/lichen-planus",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
    "lupus": {
        "name": "Lupus (Cutaneous)",
        "short_name": "Lupus",
        "risk_level": "high",
        "description": "An autoimmune disease that can cause distinctive rashes and photosensitive skin changes.",
        "explanation": (
            "Cutaneous lupus erythematosus is part of the lupus spectrum, an autoimmune condition "
            "where the immune system attacks healthy tissue. Skin findings may include a butterfly "
            "rash across the cheeks, discoid plaques, or photosensitivity. Lupus can also affect "
            "internal organs, so a comprehensive medical evaluation is essential."
        ),
        "common_signs": [
            "Butterfly-shaped rash across cheeks and nose",
            "Discoid plaques with scarring",
            "Photosensitivity (rash after sun exposure)",
            "Red, scaly patches on sun-exposed skin",
            "Mouth or nose ulcers",
        ],
        "what_it_means": (
            "Cutaneous lupus is a serious autoimmune condition that requires ongoing medical "
            "management and sun protection to prevent flares and complications."
        ),
        "when_to_see_doctor": (
            "See a rheumatologist or dermatologist promptly if you have a persistent facial rash, "
            "joint pain, fatigue, or other systemic symptoms alongside skin changes."
        ),
        "recommended_actions": [
            {
                "action": "Strictly protect skin from sun with broad-spectrum SPF 30+ sunscreen, protective clothing, and shade.",
                "source": {
                    "title": "Lupus and your skin",
                    "url": "https://www.aad.org/public/diseases/a-z/lupus-overview",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Avoid tanning beds and peak midday sun exposure, which can trigger lupus flares.",
                "source": {
                    "title": "Lupus",
                    "url": "https://www.mayoclinic.org/diseases-conditions/lupus/symptoms-causes/syc-20365789",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Seek evaluation by a rheumatologist for comprehensive testing and long-term management.",
                "source": {
                    "title": "Lupus",
                    "url": "https://www.cancer.org/cancer/risk-prevention/chemicals/lupus.html",
                    "publisher": "American Cancer Society",
                    "domain": "cancer.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Lupus",
                "url": "https://www.aad.org/public/diseases/a-z/lupus-overview",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Lupus",
                "url": "https://www.mayoclinic.org/diseases-conditions/lupus/symptoms-causes/syc-20365789",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Lupus erythematosus",
                "url": "https://dermnetnz.org/topics/lupus-erythematosus",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
    "moles": {
        "name": "Moles (Nevi)",
        "short_name": "Moles",
        "risk_level": "low",
        "description": "Common pigmented growths formed by clusters of melanocytes, usually benign.",
        "explanation": (
            "Moles (nevi) are very common and develop when pigment-producing cells cluster in the skin. "
            "Most appear during childhood and adolescence and remain stable. While the vast majority "
            "are harmless, any mole that changes in size, shape, color, or symptoms should be "
            "evaluated to rule out melanoma."
        ),
        "common_signs": [
            "Round or oval brown, tan, or black spots",
            "Uniform color and smooth borders",
            "Stable size over time",
            "Can be flat or slightly raised",
            "May have hair growing from them",
        ],
        "what_it_means": (
            "Most moles are benign, but monitoring for changes is important because melanoma can "
            "arise from existing moles or appear as new spots."
        ),
        "when_to_see_doctor": (
            "See a dermatologist for any mole that changes (ABCDE criteria), bleeds, itches persistently, "
            "or any new mole appearing after age 30."
        ),
        "recommended_actions": [
            {
                "action": "Perform monthly self-skin checks and track moles using the ABCDE criteria (Asymmetry, Border, Color, Diameter, Evolution).",
                "source": {
                    "title": "How to spot skin cancer",
                    "url": "https://www.aad.org/public/diseases/skin-cancer/find/at-risk/spot-skin-cancer",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Protect moles from excessive sun exposure with broad-spectrum sunscreen SPF 30+ and protective clothing.",
                "source": {
                    "title": "Moles",
                    "url": "https://www.skincancer.org/risk-factors/moles/",
                    "publisher": "Skin Cancer Foundation",
                    "domain": "skincancer.org",
                },
            },
            {
                "action": "Schedule an annual full-body skin examination with a dermatologist if you have many moles or a family history of melanoma.",
                "source": {
                    "title": "Melanoma",
                    "url": "https://www.mayoclinic.org/diseases-conditions/melanoma/symptoms-causes/syc-20374884",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Moles",
                "url": "https://www.aad.org/public/diseases/a-z/moles-overview",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Moles",
                "url": "https://www.skincancer.org/risk-factors/moles/",
                "publisher": "Skin Cancer Foundation",
                "domain": "skincancer.org",
            },
            {
                "title": "Melanocytic naevus",
                "url": "https://dermnetnz.org/topics/melanocytic-naevus",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
    "psoriasis": {
        "name": "Psoriasis",
        "short_name": "Psoriasis",
        "risk_level": "moderate",
        "description": "A chronic autoimmune condition causing thick, scaly, inflamed patches of skin.",
        "explanation": (
            "Psoriasis speeds up the life cycle of skin cells, causing them to build up rapidly "
            "on the surface and form scales and red patches. It is driven by immune system "
            "dysfunction and can be triggered by stress, infections, skin injury, and certain "
            "medications. Psoriasis is not contagious but is associated with joint disease (psoriatic arthritis)."
        ),
        "common_signs": [
            "Thick, silvery scales on red patches",
            "Dry, cracked skin that may bleed",
            "Itching, burning, or soreness",
            "Nail pitting or separation",
            "Joint stiffness or swelling (psoriatic arthritis)",
        ],
        "what_it_means": (
            "Psoriasis is a lifelong condition that can be well managed with treatment, though "
            "it may increase the risk of other health conditions such as arthritis."
        ),
        "when_to_see_doctor": (
            "See a dermatologist if psoriasis covers a large area, affects your quality of life, "
            "involves joints, or does not respond to basic skin care."
        ),
        "recommended_actions": [
            {
                "action": "Keep skin moisturized daily with thick, fragrance-free emollients to reduce scaling and cracking.",
                "source": {
                    "title": "Psoriasis: Tips for managing",
                    "url": "https://www.aad.org/public/diseases/psoriasis/treatment/treatment",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Avoid triggers such as skin injury, excessive alcohol, and smoking when possible.",
                "source": {
                    "title": "Psoriasis",
                    "url": "https://www.mayoclinic.org/diseases-conditions/psoriasis/symptoms-causes/syc-20354049",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Brief daily sun exposure may help some people, but always use sun protection to avoid burns.",
                "source": {
                    "title": "Psoriasis",
                    "url": "https://www.health.harvard.edu/diseases-and-conditions/psoriasis-a-to-z",
                    "publisher": "Harvard Health Publishing",
                    "domain": "health.harvard.edu",
                },
            },
        ],
        "sources": [
            {
                "title": "Psoriasis",
                "url": "https://www.aad.org/public/diseases/psoriasis",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Psoriasis",
                "url": "https://www.mayoclinic.org/diseases-conditions/psoriasis/symptoms-causes/syc-20354049",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Psoriasis",
                "url": "https://dermnetnz.org/topics/psoriasis",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
    "rosacea": {
        "name": "Rosacea",
        "short_name": "Rosacea",
        "risk_level": "moderate",
        "description": "A chronic facial condition causing redness, visible blood vessels, and sometimes acne-like bumps.",
        "explanation": (
            "Rosacea primarily affects the central face and causes persistent redness, flushing, "
            "and visible blood vessels. Triggers include sun exposure, hot drinks, spicy foods, "
            "alcohol, stress, and extreme temperatures. While not dangerous, it can worsen over "
            "time without treatment and significantly affect appearance."
        ),
        "common_signs": [
            "Persistent facial redness, especially on cheeks and nose",
            "Visible blood vessels (telangiectasia)",
            "Papules and pustules resembling acne",
            "Eye irritation (ocular rosacea)",
            "Thickened skin on the nose (rhinophyma) in advanced cases",
        ],
        "what_it_means": (
            "Rosacea is a manageable chronic condition, though it tends to flare periodically "
            "and may progress if triggers are not addressed."
        ),
        "when_to_see_doctor": (
            "See a dermatologist if facial redness is persistent, you develop eye symptoms, "
            "or over-the-counter care is not helping."
        ),
        "recommended_actions": [
            {
                "action": "Identify and avoid personal triggers such as hot beverages, spicy foods, alcohol, and extreme temperatures.",
                "source": {
                    "title": "Rosacea: Tips for managing",
                    "url": "https://www.aad.org/public/diseases/rosacea/treatment/treatment",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Use broad-spectrum sunscreen SPF 30+ daily and protect your face from wind and cold.",
                "source": {
                    "title": "Rosacea",
                    "url": "https://www.mayoclinic.org/diseases-conditions/rosacea/symptoms-causes/syc-20353851",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Use gentle, fragrance-free skin care and avoid harsh scrubs or irritating products on the face.",
                "source": {
                    "title": "Rosacea",
                    "url": "https://dermnetnz.org/topics/rosacea",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Rosacea",
                "url": "https://www.aad.org/public/diseases/rosacea",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Rosacea",
                "url": "https://www.mayoclinic.org/diseases-conditions/rosacea/symptoms-causes/syc-20353851",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Rosacea",
                "url": "https://dermnetnz.org/topics/rosacea",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
    "seborrheic_keratoses": {
        "name": "Seborrheic Keratosis",
        "short_name": "Seborrheic Keratosis",
        "risk_level": "low",
        "description": "Common benign waxy growths that appear with age and are not cancerous.",
        "explanation": (
            "Seborrheic keratoses are one of the most common non-cancerous skin growths in adults, "
            "especially after age 50. They often look waxy, stuck-on, or warty and can vary in color "
            "from tan to dark brown or black. They are harmless but can be cosmetically bothersome "
            "or irritated by clothing."
        ),
        "common_signs": [
            "Waxy, stuck-on appearance",
            "Variable color from tan to dark brown or black",
            "Rough, bumpy surface texture",
            "Round or oval shape",
            "Multiple lesions on trunk, face, or extremities",
        ],
        "what_it_means": (
            "Seborrheic keratoses are benign and do not become skin cancer, though new dark "
            "lesions should still be checked to distinguish them from melanoma."
        ),
        "when_to_see_doctor": (
            "See a dermatologist if a growth looks unusual, changes rapidly, itches, bleeds, "
            "or you want it removed for cosmetic reasons."
        ),
        "recommended_actions": [
            {
                "action": "Monitor lesions for sudden changes in appearance and have new dark spots evaluated to rule out melanoma.",
                "source": {
                    "title": "How to spot skin cancer",
                    "url": "https://www.aad.org/public/diseases/skin-cancer/find/at-risk/spot-skin-cancer",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Avoid picking or scratching lesions, which can cause irritation or infection.",
                "source": {
                    "title": "Seborrheic keratosis",
                    "url": "https://www.mayoclinic.org/diseases-conditions/seborrheic-keratosis/symptoms-causes/syc-20353878",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Consult a dermatologist if a lesion is irritated by clothing or you wish to discuss removal options.",
                "source": {
                    "title": "Seborrhoeic keratosis",
                    "url": "https://dermnetnz.org/topics/seborrhoeic-keratosis",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Seborrheic keratoses",
                "url": "https://www.aad.org/public/diseases/a-z/seborrheic-keratoses-overview",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Seborrheic keratosis",
                "url": "https://www.mayoclinic.org/diseases-conditions/seborrheic-keratosis/symptoms-causes/syc-20353878",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Seborrhoeic keratosis",
                "url": "https://dermnetnz.org/topics/seborrhoeic-keratosis",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
    "skin_cancer": {
        "name": "Skin Cancer",
        "short_name": "Skin Cancer",
        "risk_level": "high",
        "description": "Malignant growths including melanoma, basal cell carcinoma, and squamous cell carcinoma.",
        "explanation": (
            "Skin cancer develops when skin cells grow abnormally, most often due to cumulative "
            "UV radiation exposure. Melanoma arises from pigment cells and can spread if not caught "
            "early. Basal cell and squamous cell carcinomas are more common and usually grow locally "
            "but still require prompt treatment."
        ),
        "common_signs": [
            "New or changing mole (melanoma ABCDE signs)",
            "Pearly or waxy bump that may bleed (basal cell)",
            "Scaly, crusty patch that does not heal (squamous cell)",
            "Sore that persists or recurs",
            "Dark streak under a nail",
        ],
        "what_it_means": (
            "Skin cancer is potentially serious, but early detection and treatment significantly "
            "improve outcomes, especially for melanoma."
        ),
        "when_to_see_doctor": (
            "See a dermatologist immediately for any new, changing, or unusual skin lesion, "
            "especially one that bleeds, grows, or does not heal within a few weeks."
        ),
        "recommended_actions": [
            {
                "action": "Schedule a prompt dermatology appointment for evaluation of any suspicious lesion; early treatment is critical.",
                "source": {
                    "title": "Skin cancer",
                    "url": "https://www.skincancer.org/skin-cancer-information/",
                    "publisher": "Skin Cancer Foundation",
                    "domain": "skincancer.org",
                },
            },
            {
                "action": "Practice rigorous sun protection with broad-spectrum SPF 30+ sunscreen, protective clothing, and shade.",
                "source": {
                    "title": "Skin cancer",
                    "url": "https://www.aad.org/public/diseases/skin-cancer",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Perform monthly self-examinations and photograph suspicious spots to track changes over time.",
                "source": {
                    "title": "How to spot skin cancer",
                    "url": "https://www.cancer.org/cancer/types/skin-cancer/detection-diagnosis-staging/signs-and-symptoms.html",
                    "publisher": "American Cancer Society",
                    "domain": "cancer.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Skin cancer",
                "url": "https://www.skincancer.org/skin-cancer-information/",
                "publisher": "Skin Cancer Foundation",
                "domain": "skincancer.org",
            },
            {
                "title": "Skin cancer",
                "url": "https://www.aad.org/public/diseases/skin-cancer",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Skin cancer",
                "url": "https://www.mayoclinic.org/diseases-conditions/skin-cancer/symptoms-causes/syc-20377605",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
        ],
    },
    "sun_damage": {
        "name": "Sun Damage (Photoaging)",
        "short_name": "Sun Damage",
        "risk_level": "moderate",
        "description": "Premature skin aging and changes caused by long-term ultraviolet radiation exposure.",
        "explanation": (
            "Photoaging refers to cumulative UV damage that breaks down collagen and elastin, "
            "leading to wrinkles, uneven pigmentation, and rough texture. It also increases the "
            "risk of precancerous lesions and skin cancer. Damage accumulates over years of "
            "sun exposure, including tanning and sunburns."
        ),
        "common_signs": [
            "Fine lines and wrinkles",
            "Uneven pigmentation and age spots",
            "Rough, leathery skin texture",
            "Visible broken blood vessels",
            "Loss of skin elasticity",
        ],
        "what_it_means": (
            "Sun damage is largely preventable and indicates increased future risk of skin "
            "cancer and accelerated aging."
        ),
        "when_to_see_doctor": (
            "See a dermatologist for evaluation of new spots, rough patches, or if you notice "
            "significant changes in sun-exposed skin."
        ),
        "recommended_actions": [
            {
                "action": "Apply broad-spectrum sunscreen SPF 30 or higher every day, even on cloudy days, and reapply every two hours when outdoors.",
                "source": {
                    "title": "Sunscreen FAQs",
                    "url": "https://www.aad.org/media/stats-sunscreen",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Wear wide-brimmed hats, UV-protective clothing, and sunglasses when in direct sunlight.",
                "source": {
                    "title": "Sun protection",
                    "url": "https://www.skincancer.org/skin-cancer-prevention/sun-protection/",
                    "publisher": "Skin Cancer Foundation",
                    "domain": "skincancer.org",
                },
            },
            {
                "action": "Avoid tanning beds and intentional tanning, which accelerate photoaging and skin cancer risk.",
                "source": {
                    "title": "The risks of tanning",
                    "url": "https://www.health.harvard.edu/staying-healthy/the-risks-of-tanning",
                    "publisher": "Harvard Health Publishing",
                    "domain": "health.harvard.edu",
                },
            },
        ],
        "sources": [
            {
                "title": "Photoaging",
                "url": "https://dermnetnz.org/topics/photoageing",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
            {
                "title": "Sun protection",
                "url": "https://www.skincancer.org/skin-cancer-prevention/sun-protection/",
                "publisher": "Skin Cancer Foundation",
                "domain": "skincancer.org",
            },
            {
                "title": "Sunscreen FAQs",
                "url": "https://www.aad.org/media/stats-sunscreen",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
        ],
    },
    "tinea": {
        "name": "Tinea (Ringworm)",
        "short_name": "Tinea",
        "risk_level": "low",
        "description": "A contagious fungal infection causing ring-shaped, scaly rashes on the skin, scalp, or nails.",
        "explanation": (
            "Tinea, commonly called ringworm, is a fungal infection that thrives in warm, moist "
            "environments. Despite its name, it is not caused by worms. It spreads through direct "
            "skin contact or shared items like towels and gym equipment. Different species affect "
            "the body (tinea corporis), feet (athlete's foot), groin (jock itch), or scalp."
        ),
        "common_signs": [
            "Ring-shaped red, scaly patch with clearer center",
            "Itching and burning",
            "Raised, expanding border",
            "Athlete's foot: peeling between toes",
            "Nail thickening or discoloration (tinea unguium)",
        ],
        "what_it_means": (
            "Tinea is treatable with antifungal therapy but is contagious and can spread to other "
            "body areas or people without treatment."
        ),
        "when_to_see_doctor": (
            "See a doctor if over-the-counter antifungal treatment does not improve symptoms "
            "within two weeks, or if the scalp or nails are involved."
        ),
        "recommended_actions": [
            {
                "action": "Keep affected areas clean and dry; change socks and underwear daily.",
                "source": {
                    "title": "Ringworm",
                    "url": "https://www.aad.org/public/diseases/a-z/ringworm-overview",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Do not share towels, clothing, or personal items until the infection has cleared.",
                "source": {
                    "title": "Ringworm (body)",
                    "url": "https://www.mayoclinic.org/diseases-conditions/ringworm-body/symptoms-causes/syc-20353780",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Use antifungal treatment as directed by a healthcare provider and continue for the full recommended course.",
                "source": {
                    "title": "Tinea corporis",
                    "url": "https://dermnetnz.org/topics/tinea-corporis",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Ringworm",
                "url": "https://www.aad.org/public/diseases/a-z/ringworm-overview",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Ringworm (body)",
                "url": "https://www.mayoclinic.org/diseases-conditions/ringworm-body/symptoms-causes/syc-20353780",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Tinea corporis",
                "url": "https://dermnetnz.org/topics/tinea-corporis",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
    "normal": {
        "name": "Normal Skin",
        "short_name": "Normal",
        "risk_level": "low",
        "description": "Skin appearance within typical healthy variation without signs of a specific condition.",
        "explanation": (
            "A normal classification suggests the image shows skin without clear features of a "
            "recognized dermatologic condition. Healthy skin varies naturally in color, texture, "
            "and minor blemishes. This result does not replace a professional skin examination, "
            "especially if you notice any changes or symptoms."
        ),
        "common_signs": [
            "Even or naturally varied skin tone",
            "Smooth or mildly textured surface",
            "No persistent rash or lesion",
            "No significant scaling or inflammation",
            "Minor freckles or texture within normal range",
        ],
        "what_it_means": (
            "No specific skin condition was detected, though continued self-monitoring and "
            "sun protection remain good practices."
        ),
        "when_to_see_doctor": (
            "See a dermatologist if you notice any new or changing spots, persistent symptoms, "
            "or have concerns despite a normal result."
        ),
        "recommended_actions": [
            {
                "action": "Use broad-spectrum sunscreen SPF 30+ daily to protect against UV damage and reduce skin cancer risk.",
                "source": {
                    "title": "Sunscreen FAQs",
                    "url": "https://www.aad.org/media/stats-sunscreen",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Perform regular self-skin checks and note any new or changing moles or spots.",
                "source": {
                    "title": "How to spot skin cancer",
                    "url": "https://www.skincancer.org/early-detection/self-exams/",
                    "publisher": "Skin Cancer Foundation",
                    "domain": "skincancer.org",
                },
            },
            {
                "action": "Maintain gentle daily skin care with mild cleansing and moisturizing suited to your skin type.",
                "source": {
                    "title": "Skin care basics",
                    "url": "https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/skin-care/art-20048237",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Skin care basics",
                "url": "https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/skin-care/art-20048237",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Sun protection",
                "url": "https://www.skincancer.org/skin-cancer-prevention/sun-protection/",
                "publisher": "Skin Cancer Foundation",
                "domain": "skincancer.org",
            },
            {
                "title": "Sunscreen FAQs",
                "url": "https://www.aad.org/media/stats-sunscreen",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
        ],
    },
    "vascular_tumors": {
        "name": "Vascular Tumor",
        "short_name": "Vascular Tumor",
        "risk_level": "low",
        "description": "Benign blood-vessel-related growths such as hemangiomas or angiomas on the skin.",
        "explanation": (
            "Vascular tumors include benign growths made up of blood vessels, such as cherry "
            "angiomas, hemangiomas, and pyogenic granulomas. Most are harmless and appear as "
            "red or purple spots or bumps. Some may bleed easily if traumatized, and new or "
            "changing vascular lesions should be evaluated to rule out other diagnoses."
        ),
        "common_signs": [
            "Red, purple, or blue skin spots or bumps",
            "Blanching with pressure (some lesions)",
            "Smooth, dome-shaped appearance",
            "May bleed easily if bumped",
            "Stable or slowly growing over time",
        ],
        "what_it_means": (
            "Most vascular skin growths are benign, though evaluation helps distinguish them "
            "from other red lesions that may need treatment."
        ),
        "when_to_see_doctor": (
            "See a dermatologist if a vascular lesion is new, growing, bleeding frequently, "
            "or if you are uncertain about the diagnosis."
        ),
        "recommended_actions": [
            {
                "action": "Protect lesions from trauma to reduce bleeding; apply gentle pressure with a clean cloth if bleeding occurs.",
                "source": {
                    "title": "Cherry angioma",
                    "url": "https://dermnetnz.org/topics/cherry-angioma",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
            {
                "action": "Monitor for changes in size, color, or shape and photograph lesions periodically.",
                "source": {
                    "title": "How to spot skin cancer",
                    "url": "https://www.aad.org/public/diseases/skin-cancer/find/at-risk/spot-skin-cancer",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Consult a dermatologist for diagnosis if the lesion is new, changing, or causing symptoms.",
                "source": {
                    "title": "Hemangioma",
                    "url": "https://www.mayoclinic.org/diseases-conditions/hemangioma/symptoms-causes/syc-20352385",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Cherry angioma",
                "url": "https://dermnetnz.org/topics/cherry-angioma",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
            {
                "title": "Hemangioma",
                "url": "https://www.mayoclinic.org/diseases-conditions/hemangioma/symptoms-causes/syc-20352385",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Vascular lesions",
                "url": "https://www.aad.org/public/diseases/a-z/vascular-birthmarks-overview",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
        ],
    },
    "vasculitis": {
        "name": "Vasculitis",
        "short_name": "Vasculitis",
        "risk_level": "high",
        "description": "Inflammation of blood vessels that can cause skin rashes, purpura, and systemic complications.",
        "explanation": (
            "Cutaneous vasculitis occurs when blood vessel walls become inflamed, leading to "
            "redness, purpura (non-blanching spots), ulcers, or livedo patterns. It may be limited "
            "to the skin or signal a systemic autoimmune or infectious process affecting internal "
            "organs. Prompt diagnosis is important to identify the underlying cause."
        ),
        "common_signs": [
            "Non-blanching purple or red spots (purpura)",
            "Palpable purpura (raised purple spots)",
            "Skin ulcers or necrosis",
            "Livedo reticularis (net-like pattern)",
            "Accompanying fever, joint pain, or fatigue",
        ],
        "what_it_means": (
            "Vasculitis can range from mild skin-limited disease to a serious systemic condition "
            "requiring urgent medical evaluation and treatment."
        ),
        "when_to_see_doctor": (
            "Seek prompt medical care for new purpura, especially with fever, joint pain, "
            "abdominal pain, or if spots do not blanch when pressed."
        ),
        "recommended_actions": [
            {
                "action": "Seek urgent medical evaluation for new non-blanching spots, especially with systemic symptoms.",
                "source": {
                    "title": "Vasculitis",
                    "url": "https://www.mayoclinic.org/diseases-conditions/vasculitis/symptoms-causes/syc-20363435",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Avoid self-diagnosis; vasculitis requires blood tests and often a skin biopsy for proper diagnosis.",
                "source": {
                    "title": "Cutaneous vasculitis",
                    "url": "https://dermnetnz.org/topics/cutaneous-vasculitis",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
            {
                "action": "Follow up with a rheumatologist or dermatologist for ongoing management if systemic vasculitis is diagnosed.",
                "source": {
                    "title": "Vasculitis",
                    "url": "https://www.health.harvard.edu/diseases-and-conditions/vasculitis-a-to-z",
                    "publisher": "Harvard Health Publishing",
                    "domain": "health.harvard.edu",
                },
            },
        ],
        "sources": [
            {
                "title": "Cutaneous vasculitis",
                "url": "https://dermnetnz.org/topics/cutaneous-vasculitis",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
            {
                "title": "Vasculitis",
                "url": "https://www.mayoclinic.org/diseases-conditions/vasculitis/symptoms-causes/syc-20363435",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Vasculitis",
                "url": "https://www.health.harvard.edu/diseases-and-conditions/vasculitis-a-to-z",
                "publisher": "Harvard Health Publishing",
                "domain": "health.harvard.edu",
            },
        ],
    },
    "vitiligo": {
        "name": "Vitiligo",
        "short_name": "Vitiligo",
        "risk_level": "low",
        "description": "An autoimmune condition causing loss of skin pigment in patchy white areas.",
        "explanation": (
            "Vitiligo occurs when melanocytes (pigment-producing cells) are destroyed, leading "
            "to well-defined white patches on the skin. It is not contagious or life-threatening "
            "but can affect appearance and sun sensitivity in depigmented areas. It may be "
            "associated with other autoimmune conditions such as thyroid disease."
        ),
        "common_signs": [
            "Well-defined white patches on skin",
            "Premature whitening of hair in affected areas",
            "Symmetrical distribution (common)",
            "Loss of color in mouth or eye tissues",
            "Increased sun sensitivity in white patches",
        ],
        "what_it_means": (
            "Vitiligo is a benign but often persistent condition that affects skin color rather "
            "than overall health, though sun protection in affected areas is important."
        ),
        "when_to_see_doctor": (
            "See a dermatologist for diagnosis and treatment options, especially if patches "
            "are spreading or affecting your quality of life."
        ),
        "recommended_actions": [
            {
                "action": "Apply broad-spectrum sunscreen SPF 30+ to depigmented areas, which burn more easily than surrounding skin.",
                "source": {
                    "title": "Vitiligo: Diagnosis and treatment",
                    "url": "https://www.aad.org/public/diseases/a-z/vitiligo-overview",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Protect affected skin from sunburn with clothing and shade in addition to sunscreen.",
                "source": {
                    "title": "Vitiligo",
                    "url": "https://www.mayoclinic.org/diseases-conditions/vitiligo/symptoms-causes/syc-20355912",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Consult a dermatologist about treatment options if you wish to repigment or stabilize spreading patches.",
                "source": {
                    "title": "Vitiligo",
                    "url": "https://dermnetnz.org/topics/vitiligo",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Vitiligo",
                "url": "https://www.aad.org/public/diseases/a-z/vitiligo-overview",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Vitiligo",
                "url": "https://www.mayoclinic.org/diseases-conditions/vitiligo/symptoms-causes/syc-20355912",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Vitiligo",
                "url": "https://dermnetnz.org/topics/vitiligo",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
    "warts": {
        "name": "Warts",
        "short_name": "Warts",
        "risk_level": "low",
        "description": "Rough, raised growths caused by human papillomavirus (HPV) infection of the skin.",
        "explanation": (
            "Warts are benign skin growths caused by HPV entering through small cuts or breaks "
            "in the skin. They are contagious and can spread to other body areas or people through "
            "direct contact. Most warts resolve on their own over time, but treatment can speed "
            "clearance and reduce spread."
        ),
        "common_signs": [
            "Rough, grainy raised bump",
            "Flesh-colored, white, or brown appearance",
            "Black dots (clotted blood vessels) on surface",
            "Common on hands, feet (plantar warts), or face",
            "May be painful when on weight-bearing areas",
        ],
        "what_it_means": (
            "Warts are generally harmless and often resolve without treatment, though they "
            "can persist and spread without intervention."
        ),
        "when_to_see_doctor": (
            "See a dermatologist if warts are painful, spreading, on the face or genitals, "
            "or if you have diabetes or a weakened immune system."
        ),
        "recommended_actions": [
            {
                "action": "Avoid picking at warts to prevent spreading the virus to other areas or people.",
                "source": {
                    "title": "Warts",
                    "url": "https://www.aad.org/public/diseases/a-z/warts-overview",
                    "publisher": "American Academy of Dermatology",
                    "domain": "aad.org",
                },
            },
            {
                "action": "Keep feet dry and wear flip-flops in shared showers or pool areas to reduce spread.",
                "source": {
                    "title": "Plantar warts",
                    "url": "https://www.mayoclinic.org/diseases-conditions/plantar-warts/symptoms-causes/syc-20352691",
                    "publisher": "Mayo Clinic",
                    "domain": "mayoclinic.org",
                },
            },
            {
                "action": "Consult a dermatologist for treatment options if warts persist, multiply, or cause discomfort.",
                "source": {
                    "title": "Viral warts",
                    "url": "https://dermnetnz.org/topics/viral-warts",
                    "publisher": "DermNet NZ",
                    "domain": "dermnetnz.org",
                },
            },
        ],
        "sources": [
            {
                "title": "Warts",
                "url": "https://www.aad.org/public/diseases/a-z/warts-overview",
                "publisher": "American Academy of Dermatology",
                "domain": "aad.org",
            },
            {
                "title": "Plantar warts",
                "url": "https://www.mayoclinic.org/diseases-conditions/plantar-warts/symptoms-causes/syc-20352691",
                "publisher": "Mayo Clinic",
                "domain": "mayoclinic.org",
            },
            {
                "title": "Viral warts",
                "url": "https://dermnetnz.org/topics/viral-warts",
                "publisher": "DermNet NZ",
                "domain": "dermnetnz.org",
            },
        ],
    },
}
