# =========================================================
# City Normalization Mapping - كل محافظات ومدن مصر
# كل قرية / حي / منطقة أثرية بترجع للمدينة الأم بتاعتها
# =========================================================

CAIRO_DISTRICTS = [
    "القاهرة", "قسم قصر النيل", "قسم عابدين", "قسم الموسكي", "قسم الأزبكية", "قسم بولاق",
    "قسم السيدة زينب", "قسم الخليفة", "قسم مصر القديمة", "قسم الجمالية", "الجمالية", "الحسين",
    "عابدين", "باب اللوق", "وسط البلد", "مدينة نصر", "مصر الجديدة", "المعادي", "الزمالك", "الدقي",
    "المقطم", "حلوان", "شبرا", "روض الفرج", "عين شمس", "المطرية", "التجمع الخامس", "القاهرة الجديدة",
    "مدينتي", "الشروق", "بدر", "العبور",
    "Cairo", "Downtown Cairo", "Heliopolis", "Nasr City", "Zamalek", "Garden City", "Old Cairo",
    "Maadi", "Dokki", "Mokattam", "Helwan", "Shubra", "Ain Shams", "New Cairo", "Madinaty",
    "El Shorouk", "Badr City", "Obour City",
]

GIZA_DISTRICTS = [
    "الجيزة", "الهرم", "6 أكتوبر", "الشيخ زايد", "أكتوبر", "فيصل", "إمبابة", "بولاق الدكرور",
    "العجوزة", "الوراق", "أوسيم", "كرداسة", "أبو رواش", "منشأة القناطر",
    "Giza", "Al Haram", "Pyramids", "6th of October", "Sheikh Zayed", "Faisal", "Imbaba",
    "Boulaq El Dakrour", "Agouza", "Warraq", "Ausim", "Kerdasa",
]

ALEXANDRIA_DISTRICTS = [
    "الإسكندرية", "سيدي جابر", "محرم بك", "الرمل", "المنتزه", "العجمي", "برج العرب", "ستانلي",
    "سيدي بشر", "كرموز", "اللبان", "المندرة", "أبو قير", "المعمورة", "جليم", "سموحة",
    "Alexandria", "Sidi Gaber", "Montaza", "Agami", "Borg El Arab", "Stanley", "Sidi Bishr",
    "Gleem", "Smouha", "Abu Qir", "Miami",
]

LUXOR_DISTRICTS = [
    "الأقصر", "الأقصر الجديدة", "مدينه القرنة الجديدة", "القرنة", "القرنة الجديدة", "الكرنك",
    "البر الغربي", "البر الشرقي", "طيبة", "ديروط الشريف", "أرمنت", "الطود", "إسنا", "الزينية",
    "Luxor", "New Luxor", "Karnak", "Karnak New", "Karnak Old", "West Bank", "East Bank",
    "Qurna", "New Qurna", "El Qurna", "Thebes", "Armant", "Esna", "Al Zeiniya",
]

ASWAN_DISTRICTS = [
    "أسوان", "أسوان الجديدة", "إدفو", "كوم أمبو", "دراو", "أبو سمبل", "النوبة", "السد العالي",
    "جزيرة الفنتين", "جزيرة النباتات", "جزيرة إلفنتين", "جزيرة كتشنر",
    "Aswan", "New Aswan", "Edfu", "Kom Ombo", "Daraw", "Abu Simbel", "Nubia", "High Dam",
    "Elephantine Island", "Kitchener's Island",
]

HURGHADA_DISTRICTS = [
    "الغردقة", "سهل حشيش", "الجونة", "مكادي باي", "سفاجا", "القصير", "مرسى علم",
    "Hurghada", "Sahl Hasheesh", "El Gouna", "Makadi Bay", "Safaga", "El Quseir", "Marsa Alam",
    "Soma Bay",
]

RED_SEA_OTHER_DISTRICTS = [
    "رأس غارب", "شلاتين", "حلايب",
    "Ras Gharib", "Shalateen", "Halayeb",
]

SHARM_EL_SHEIKH_DISTRICTS = [
    "شرم الشيخ", "نعمة باي", "شرم الماية", "نبق", "رأس محمد",
    "Sharm El Sheikh", "Naama Bay", "Sharm El Maya", "Nabq", "Ras Mohamed",
]

DAHAB_DISTRICTS = [
    "دهب", "أسله", "لاجونا", "مشربة",
    "Dahab", "Assalah", "Laguna", "Mashraba",
]

SOUTH_SINAI_OTHER_DISTRICTS = [
    "طابا", "نويبع", "سانت كاترين", "طور سيناء",
    "Taba", "Nuweiba", "Saint Catherine", "St. Catherine", "Tor Sinai",
]

NORTH_SINAI_DISTRICTS = [
    "العريش", "الشيخ زويد", "رفح", "بئر العبد",
    "Arish", "El Arish", "Sheikh Zuweid", "Rafah", "Bir al-Abd",
]

ISMAILIA_DISTRICTS = [
    "الإسماعيلية", "فايد", "القنطرة شرق", "القنطرة غرب", "التل الكبير", "أبو صوير",
    "Ismailia", "Fayed", "Qantara East", "Qantara West", "Abu Suwir",
]

SUEZ_DISTRICTS = [
    "السويس", "عتاقة", "الجناين", "فيصل", "الأربعين",
    "Suez", "Ataqa", "Ganayen", "Arbaeen",
]

PORT_SAID_DISTRICTS = [
    "بورسعيد", "بورفؤاد", "الزهور", "الشرق", "المناخ", "الضواحي", "العرب",
    "Port Said", "Port Fouad", "El Zohour", "El Sharq", "El Manakh", "El Dawahy", "El Arab",
]

DAMIETTA_DISTRICTS = [
    "دمياط", "دمياط الجديدة", "رأس البر", "فارسكور", "الزرقا", "كفر سعد", "كفر البطيخ",
    "Damietta", "New Damietta", "Ras El Bar", "Faraskur", "Ezbet El Borg",
]

DAKAHLIA_DISTRICTS = [
    "المنصورة", "طلخا", "ميت غمر", "دكرنس", "أجا", "منية النصر", "السنبلاوين", "بلقاس",
    "شربين", "المطرية", "منشية دياب", "تمي الأمديد", "الجمالية", "بني عبيد",
    "Mansoura", "El Mansoura", "Talkha", "Mit Ghamr", "Dekernes", "Aga", "Senbellawein",
    "Belqas", "Sherbin",
]

SHARQIA_DISTRICTS = [
    "الزقازيق", "العاشر من رمضان", "بلبيس", "منيا القمح", "أبو حماد", "أبو كبير", "الإبراهيمية",
    "الحسينية", "الصالحية الجديدة", "ديرب نجم", "فاقوس", "كفر صقر", "مشتول السوق", "ههيا",
    "Zagazig", "10th of Ramadan", "Belbeis", "Minya El Qamh", "Abu Hammad", "Abu Kabir",
    "Faqous", "Kafr Saqr", "Hihya",
]

GHARBIA_DISTRICTS = [
    "طنطا", "المحلة الكبرى", "كفر الزيات", "زفتى", "السنطة", "بسيون", "قطور",
    "Tanta", "El Mahalla El Kubra", "Kafr El Zayat", "Zefta", "El Santa", "Basyoun", "Qotour",
]

MONUFIA_DISTRICTS = [
    "شبين الكوم", "منوف", "أشمون", "الباجور", "بركة السبع", "تلا", "قويسنا", "السادات",
    "Shibin El Kom", "Menouf", "Ashmoun", "El Bagour", "Berket El Sabaa", "Tala", "Quesna",
    "Sadat City",
]

QALYUBIA_DISTRICTS = [
    "بنها", "شبرا الخيمة", "القناطر الخيرية", "قليوب", "طوخ", "كفر شكر", "الخانكة", "العبور",
    "Banha", "Shubra El Kheima", "Qanater", "Qalyub", "Toukh", "Kafr Shukr", "El Khanka",
]

BEHEIRA_DISTRICTS = [
    "دمنهور", "كفر الدوار", "رشيد", "إدكو", "أبو حمص", "أبو المطامير", "المحمودية", "إيتاي البارود",
    "حوش عيسى", "شبراخيت", "الدلنجات", "النوبارية", "وادي النطرون",
    "Damanhour", "Kafr El Dawwar", "Rashid", "Rosetta", "Edko", "Abu Hummus", "Wadi El Natrun",
]

KAFR_EL_SHEIKH_DISTRICTS = [
    "كفر الشيخ", "دسوق", "فوه", "مطوبس", "بلطيم", "الحامول", "بيلا", "الرياض", "قلين", "سيدي سالم",
    "Kafr El Sheikh", "Desouk", "Fuwwah", "Metoubes", "Baltim", "Hamoul", "Bila", "Riyadh",
]

BENI_SUEF_DISTRICTS = [
    "بني سويف", "الواسطى", "ناصر", "إهناسيا", "ببا", "الفشن", "سمسطا",
    "Beni Suef", "El Wasta", "Nasser", "Ihnasia", "Beba", "El Fashn", "Somasta",
]

FAYOUM_DISTRICTS = [
    "الفيوم", "طامية", "سنورس", "إطسا", "يوسف الصديق", "أبشواي", "سيلا", "سنورس", "قارون",
    "وادي الريان", "تونس",
    "Fayoum", "El Fayoum", "Tamiya", "Sinnuris", "Itsa", "Ibsheway", "Lake Qarun",
    "Wadi El Rayan", "Tunis Village",
]

MINYA_DISTRICTS = [
    "المنيا", "ملوي", "بني مزار", "مغاغة", "سمالوط", "مطاي", "أبو قرقاص", "دير مواس",
    "تونا الجبل", "بني حسن", "العمارنة",
    "Minya", "El Minya", "Mallawi", "Beni Mazar", "Maghagha", "Samalut", "Matai",
    "Tuna El Gebel", "Beni Hasan", "Amarna", "El Amarna",
]

ASSIUT_DISTRICTS = [
    "أسيوط", "ديروط", "منفلوط", "القوصية", "أبنوب", "أبو تيج", "الغنايم", "ساحل سليم", "البداري",
    "صدفا",
    "Assiut", "Asyut", "Dairut", "Manfalut", "Qusiya", "Abnub", "Abu Tig", "El Badari", "Sedfa",
]

SOHAG_DISTRICTS = [
    "سوهاج", "أخميم", "جرجا", "طهطا", "طما", "المراغة", "دار السلام", "ساقلته", "البلينا", "جهينة",
    "Sohag", "Akhmim", "Girga", "Tahta", "Tama", "El Maragha", "Dar El Salam", "Saqultah",
    "El Balyana",
]

QENA_DISTRICTS = [
    "قنا", "نجع حمادي", "قوص", "نقادة", "دشنا", "أبو تشت", "فرشوط", "الوقف",
    "Qena", "Nag Hammadi", "Qus", "Naqada", "Dishna", "Abu Tesht", "Farshut",
]

NEW_VALLEY_DISTRICTS = [
    "الخارجة", "الداخلة", "الفرافرة", "باريس", "بلاط",
    "El Kharga", "Kharga", "Dakhla", "Farafra", "Paris Oasis", "Balat",
]

MATROUH_DISTRICTS = [
    "مرسى مطروح", "العلمين", "سيدي براني", "السلوم", "سيوة", "النجيلة", "الضبعة",
    "Marsa Matrouh", "El Alamein", "Sidi Barrani", "Sallum", "Siwa", "Siwa Oasis", "El Dabaa",
]

# =========================================================
# Master mapping: district/village/area -> parent city
# =========================================================
CITY_DISTRICT_MAP: dict[str, str] = {}

def _register(parent_city: str, districts: list[str]) -> None:
    for d in districts:
        CITY_DISTRICT_MAP[d.strip()] = parent_city
    # المدينة نفسها ترجع لنفسها (identity)
    CITY_DISTRICT_MAP[parent_city] = parent_city

_register("Cairo", CAIRO_DISTRICTS)
_register("Giza", GIZA_DISTRICTS)
_register("Alexandria", ALEXANDRIA_DISTRICTS)
_register("Luxor", LUXOR_DISTRICTS)
_register("Aswan", ASWAN_DISTRICTS)
_register("Hurghada", HURGHADA_DISTRICTS)
_register("Red Sea", RED_SEA_OTHER_DISTRICTS)
_register("Sharm El Sheikh", SHARM_EL_SHEIKH_DISTRICTS)
_register("Dahab", DAHAB_DISTRICTS)
_register("South Sinai", SOUTH_SINAI_OTHER_DISTRICTS)
_register("North Sinai", NORTH_SINAI_DISTRICTS)
_register("Ismailia", ISMAILIA_DISTRICTS)
_register("Suez", SUEZ_DISTRICTS)
_register("Port Said", PORT_SAID_DISTRICTS)
_register("Damietta", DAMIETTA_DISTRICTS)
_register("Mansoura", DAKAHLIA_DISTRICTS)
_register("Zagazig", SHARQIA_DISTRICTS)
_register("Tanta", GHARBIA_DISTRICTS)
_register("Shibin El Kom", MONUFIA_DISTRICTS)
_register("Banha", QALYUBIA_DISTRICTS)
_register("Damanhour", BEHEIRA_DISTRICTS)
_register("Kafr El Sheikh", KAFR_EL_SHEIKH_DISTRICTS)
_register("Beni Suef", BENI_SUEF_DISTRICTS)
_register("Fayoum", FAYOUM_DISTRICTS)
_register("Minya", MINYA_DISTRICTS)
_register("Assiut", ASSIUT_DISTRICTS)
_register("Sohag", SOHAG_DISTRICTS)
_register("Qena", QENA_DISTRICTS)
_register("New Valley", NEW_VALLEY_DISTRICTS)
_register("Matrouh", MATROUH_DISTRICTS)


# =========================================================
# قائمة المدن السياحية "الرسمية" اللي الـ LLM المفروض يختار منها
# =========================================================
TOURISTIC_CITIES: list[str] = sorted(set(CITY_DISTRICT_MAP.values()))


def normalize_city(city: str | None) -> str | None:
    """
    بترجع اسم المدينة الأم الرسمي بدل أي حي/قرية/منطقة أثرية.
    لو الاسم مش موجود في الماب، بترجعه زي ما هو (fallback).
    """
    if not city:
        return city
    cleaned = city.strip()
    return CITY_DISTRICT_MAP.get(cleaned, cleaned)