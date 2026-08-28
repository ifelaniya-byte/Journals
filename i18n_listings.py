# Quiet Mind Press — storefront copy. PDF interiors stay English.
# langs: zh 简体中文 · hi हिन्दी · es español · fr français · ha Hausa · yo Yorùbá

LANGS = {'zh': {'name': '简体中文', 'imprint': '静心出版社（Quiet Mind Press）', 'undated': '无日期，任何一天都可以开始。', 'pdf': '这是平装本的家用打印 PDF，不是可重排的电子书。', 'disclaimer': '仅供个人记录。非医疗建议，非治疗方案，与任何挑战品牌或药厂无关。', 'series_j': '静心日记（Quiet Mind Journals）', 'series_c': '静心填色（Quiet Mind Color）', 'inside': '内容', 'price': '建议售价'}, 'hi': {'name': 'हिन्दी', 'imprint': 'क्वाइट माइंड प्रेस (Quiet Mind Press)', 'undated': 'बिना तारीख — किसी भी दिन शुरू करें।', 'pdf': 'यह पेपरबैक की प्रिंट-एट-होम PDF है, रिफ़्लोएबल ईबुक नहीं।', 'disclaimer': 'केवल व्यक्तिगत उपयोग। चिकित्सा सलाह नहीं। उपचार प्रोटोकॉल नहीं। किसी ब्रांड या निर्माता से संबद्ध नहीं।', 'series_j': 'Quiet Mind Journals', 'series_c': 'Quiet Mind Color', 'inside': 'अंदर', 'price': 'सुझाई कीमत'}, 'es': {'name': 'español', 'imprint': 'Quiet Mind Press', 'undated': 'Sin fechas: empieza cualquier día.', 'pdf': 'PDF para imprimir en casa del rústico, no un ebook reajustable.', 'disclaimer': 'Uso personal. No es consejo médico ni un protocolo de tratamiento. Sin afiliación a marcas ni laboratorios.', 'series_j': 'Quiet Mind Journals', 'series_c': 'Quiet Mind Color', 'inside': 'Dentro', 'price': 'Precio sugerido'}, 'fr': {'name': 'français', 'imprint': 'Quiet Mind Press', 'undated': 'Non daté : commencez n’importe quel jour.', 'pdf': 'PDF à imprimer chez soi du broché, pas un ebook reflowable.', 'disclaimer': 'Usage personnel. Pas un avis médical, pas un protocole de traitement. Aucune affiliation à une marque ou un laboratoire.', 'series_j': 'Quiet Mind Journals', 'series_c': 'Quiet Mind Color', 'inside': 'À l’intérieur', 'price': 'Prix suggéré'}, 'ha': {'name': 'Hausa', 'imprint': 'Quiet Mind Press', 'undated': 'Babu kwanan wata — fara ko wace rana.', 'pdf': 'Wannan PDF ce ta bugu a gida na littafin faffadan fuska, ba e-littafi mai sake tsari ba.', 'disclaimer': 'Don amfani na kashin kai kawai. Ba shawarar likita ba. Ba tsarin magani ba. Babu alaƙa da wani alama ko kamfani.', 'series_j': 'Quiet Mind Journals', 'series_c': 'Quiet Mind Color', 'inside': 'A ciki', 'price': 'Farashin da aka ba da shawara'}, 'yo': {'name': 'Yorùbá', 'imprint': 'Quiet Mind Press', 'undated': 'Kò ní ọjọ́ — bẹ̀rẹ̀ ní ọjọ́ èyíkéyìí.', 'pdf': 'Èyí jẹ́ PDF tí o lè tẹ̀ ní ilé, kì í ṣe ìwé-eléktrónííkì tó ń yí iṣẹ́po padà.', 'disclaimer': 'Fun ìlò ara ẹni nikan. Kì í ṣe ìmọ̀ràn ìṣègùn. Kì í ṣe ìlànà ìtọ́jú. Kò sí àjọṣe pẹ̀lú àmì-ọjà tàbí ilé-iṣẹ́ oògùn.', 'series_j': 'Quiet Mind Journals', 'series_c': 'Quiet Mind Color', 'inside': 'Nínú', 'price': 'Iye owó tí a dábàá'}}

# n -> lang -> title, subtitle, hook, kw[7]
COPY = {
    "1": {
        "zh": {"t": '五分钟倾倒', "s": '200页轮换式五分钟提示，无日期', "h": '每页不超过五分钟。没有长提示，没有作文。只有头脑倾倒、身体核对、心情圆圈和小小胜利。', "k": ['五分钟日记', 'ADHD头脑倾倒', '微日记', '低负担日记本', '无日期日记', '讨厌写日记', '短提示笔记本']},
        "hi": {"t": 'पाँच मिनट डंप', "s": '200 पेज घूमते पाँच-मिनट प्रॉम्प्ट, बिना तारीख', "h": 'हर पन्ना पाँच मिनट या उससे कम। लंबे प्रॉम्प्ट नहीं, निबंध नहीं। सिर्फ़ ब्रेन-डंप, बॉडी-चेक, मूड सर्कल।', "k": ['5 मिनट जर्नल', 'ADHD ब्रेन डंप', 'माइक्रो जर्नल', 'कम मेहनत डायरी', 'बिना तारीख जर्नल', 'जर्नलिंग नापसंद', 'छोटे प्रॉम्प्ट']},
        "es": {"t": 'El vaciado de 5 minutos', "s": '200 páginas de prompts rotativos de cinco minutos, sin fechas', "h": 'Cada página, cinco minutos o menos. Sin ensayos. Volcados, chequeos del cuerpo, círculos de ánimo y mini logros.', "k": ['diario 5 minutos', 'brain dump TDAH', 'micro diario', 'diario fácil', 'diario sin fechas', 'odiar escribir diario', 'prompts cortos']},
        "fr": {"t": 'Le dump de 5 minutes', "s": '200 pages de prompts tournants de cinq minutes, non daté', "h": 'Chaque page : cinq minutes ou moins. Pas de longs prompts. Vidage de tête, check du corps, ronds d’humeur.', "k": ['journal 5 minutes', 'brain dump TDAH', 'micro journal', 'journal facile', 'journal non daté', 'détester écrire', 'prompts courts']},
        "ha": {"t": 'Zubarwa na minti 5', "s": 'Shafi 200 na tambayoyin minti biyar masu juyawa, babu kwanan wata', "h": 'Kowane shafi minti biyar ko ƙasa. Babu dogon rubutu. Zubar da tunani, duba jiki, da ƙananan nasaba.', "k": ['diary minti 5', 'ADHD brain dump', 'micro journal', 'diary mai sauƙi', 'babu kwanan wata', 'ƙi rubuta diary', 'gajerun tambayoyi']},
        "yo": {"t": 'Ìdàáṣẹ̀ ìṣẹ́jú 5', "s": 'Ojú-ìwé 200 ti ìbéèrè ìṣẹ́jú márùn-ún tí ó ń yí, láìsí ọjọ́', "h": 'Ojú-ìwé kọ̀ọ̀kan: ìṣẹ́jú márùn-ún tàbí kéré. Kò sí àyọkà gígùn. Ìtújáde ọpọlọ, ìyẹ̀wò ara, àti àṣeyọrí kékeré.', "k": ['ìwé ìṣẹ́jú 5', 'ADHD brain dump', 'micro journal', 'ìwé ọjọ́ rọrùn', 'láìsí ọjọ́', 'kò fẹ́ kọ ìwé', 'ìbéèrè kúkúrú']},
    },
    "2": {
        "zh": {"t": '平行生活', "s": '160页左右对照提示：发生了什么，感受如何', "h": '对页日记：一边记下发生的事，一边记下感受。给过度思考的人。', "k": ['左右对照日记', '双栏疗愈日记', 'CBT日记', '分栏笔记本', '过度思考', '两种视角', '自我觉察']},
        "hi": {"t": 'समानांतर जीवन', "s": '160 पेज साथ-साथ प्रॉम्प्ट: क्या हुआ और कैसा लगा', "h": 'स्प्लिट-पेज जर्नल: घटना और भावना साथ-साथ। ओवरथिंकिंग के लिए।', "k": ['साइड बाय साइड जर्नल', 'दो कॉलम थेरेपी', 'CBT जर्नल', 'स्प्लिट पेज', 'ओवरथिंकिंग', 'दो दृष्टिकोण', 'सेल्फ अवेयरनेस']},
        "es": {"t": 'Vidas paralelas', "s": '160 páginas de prompts en dos columnas: lo que pasó y cómo se sintió', "h": 'Un diario de dos columnas para lo ocurrido y lo sentido. Para quien da vueltas a todo.', "k": ['diario dos columnas', 'diario terapia', 'CBT diario', 'página partida', 'sobrepensar', 'dos perspectivas', 'autoconocimiento']},
        "fr": {"t": 'Vies parallèles', "s": "160 pages de prompts côte à côte : ce qui s'est passé et ce que ça a fait", "h": 'Journal deux colonnes : faits d’un côté, ressenti de l’autre. Pour ruminer moins seul.', "k": ['journal deux colonnes', 'journal thérapie', 'CBT journal', 'page splittée', 'surpenser', 'deux perspectives', 'conscience de soi']},
        "ha": {"t": 'Rayuka biyu', "s": 'Shafi 160 na tambayoyi gefe-gefe: abin da ya faru da yadda yake ji', "h": 'Diary mai ginshiƙai biyu — abin da ya faru da ji. Ga masu yawan tunani.', "k": ['diary ginshiƙai biyu', 'therapy journal', 'CBT', 'split page', 'yawan tunani', 'hannu biyu', 'sanin kai']},
        "yo": {"t": 'Ìgbésí ayé méjì', "s": 'Ojú-ìwé 160 ti ìbéèrè pẹ̀lú-opọ̀: ohun tó ṣẹlẹ̀ àti bí ó ṣe rí', "h": 'Ìwé àkọsílẹ̀ òpó méjì — ìṣẹ̀lẹ̀ níhìn-ín, ìmọ̀lara níbẹ̀. Fún ẹni tó ń rò púpọ̀.', "k": ['ìwé òpó méjì', 'therapy journal', 'CBT', 'split page', 'ríò púpọ̀', 'ojú méjì', 'ìmọ̀ ara ẹni']},
    },
    "3": {
        "zh": {"t": '夜页', "s": '5×8床头口袋日记，写给停不下来的念头', "h": '床头口袋本。给跑不完的念头和睡不着的夜。无日期。', "k": ['失眠日记', '凌晨三点', '睡不着笔记本', '念头狂奔', '床头口袋本', '夜间焦虑', '担心倾倒']},
        "hi": {"t": 'रात के पन्ने', "s": '5×8 जेबी बेडसाइड जर्नल, दौड़ते विचारों के लिए', "h": 'बेडसाइड पॉकेट बुक। दौड़ते विचारों और नींद न आने वाली रातों के लिए।', "k": ['अनिद्रा जर्नल', '3 बजे रात', 'नींद नहीं आती', 'रेसिंग थॉट्स', 'पॉकेट जर्नल', 'रात की चिंता', 'वरी डंप']},
        "es": {"t": 'Las páginas de la noche', "s": 'Diario de bolsillo 5×8 de mesita para pensamientos acelerados', "h": 'Cuaderno de mesita. Para pensamientos que no paran y noches en vela.', "k": ['diario insomnio', '3 de la madrugada', 'no puedo dormir', 'pensamientos rápidos', 'diario de bolsillo', 'ansiedad nocturna', 'vaciar preocupaciones']},
        "fr": {"t": 'Les pages de la nuit', "s": 'Journal de poche 5×8 de chevet pour les pensées qui courent', "h": 'Carnet de chevet. Pour les pensées qui courent et les nuits blanches.', "k": ['journal insomnie', '3 heures du matin', 'pas dormir', 'pensées qui courent', 'journal de poche', 'anxiété nocturne', 'vider les soucis']},
        "ha": {"t": 'Shafukan dare', "s": 'Diary ɗan aljihu 5×8 na gefen gado ga tunani masu gudu', "h": 'Littafi na gefen gado. Ga tunani masu gudu da dare babu barci.', "k": ['diary rashin barci', 'karfe 3', 'ba barci', 'tunani masu gudu', 'pocket journal', 'damuwa dare', 'zubar da damuwa']},
        "yo": {"t": 'Àwọn ojú-ìwé alẹ́', "s": 'Ìwé àpò 5×8 tí ó jọwọ́ ibùsùn fún èrò tó ń sáré', "h": 'Ìwé ẹ̀gbẹ́ ibùsùn. Fún èrò tó ń sáré àti alẹ́ tí kò jẹ́ kí o sùn.', "k": ['ìwé àìsùn', 'aago mẹ́ta', 'kò le sùn', 'èrò sáré', 'ìwé àpò', 'àníyàn alẹ́', 'ìtújáde àníyàn']},
    },
    "4": {
        "zh": {"t": '第一笔', "s": '37个超简单图案，每页3–5个大形状', "h": '超简单大色块。粗线，适合马克笔。成人入门，不是儿童书。', "k": ['成人简易填色', '入门填色书', '粗线填色', '大形状', '长辈填色', '第一本填色', '马克笔友好']},
        "hi": {"t": 'पहली रेखाएँ', "s": '37 बेहद आसान डिज़ाइन, हर पेज पर 3–5 बड़ी आकृतियाँ', "h": 'बहुत सरल बड़े आकार। मोटी रेखाएँ, मार्कर के लिए। वयस्क शुरुआती।', "k": ['आसान कलरिंग बुक', 'बिगिनर कलरिंग', 'मोटी लाइनें', 'बड़े आकार', 'सीनियर्स कलरिंग', 'पहली कलरिंग बुक', 'मार्कर फ्रेंडली']},
        "es": {"t": 'Primeros trazos', "s": '37 diseños súper fáciles con 3 a 5 formas grandes por página', "h": 'Formas grandes y simples. Líneas gruesas, bien para rotulador. Principiantes adultos.', "k": ['colorear fácil adultos', 'principiantes colorear', 'líneas gruesas', 'formas grandes', 'colorear mayores', 'primer libro colorear', 'rotulador']},
        "fr": {"t": 'Premiers traits', "s": '37 motifs très simples, 3 à 5 grandes formes par page', "h": 'Grandes formes simples. Traits épais, OK feutres. Débutants adultes.', "k": ['coloriage facile adultes', 'débutant coloriage', 'traits épais', 'grandes formes', 'coloriage seniors', 'premier coloriage', 'feutres']},
        "ha": {"t": 'Farkon zane', "s": 'Zane-zane 37 masu sauƙi gaske, manyan siffofi 3–5 a kowane shafi', "h": 'Manyan siffofi masu sauƙi. Layuka masu kauri, don marker. Manya masu farawa.', "k": ['launi mai sauƙi', 'beginner coloring', 'layuka masu kauri', 'manyán siffofi', 'launi ga tsofaffi', 'farkon littafin launi', 'marker']},
        "yo": {"t": 'Àwọn ìlà àkọ́kọ́', "s": 'Àwọn àpẹẹrẹ 37 rọrùn púpọ̀, àwọn àpẹẹrẹ ńlá 3–5 lórí ojú-ìwé kọ̀ọ̀kan', "h": 'Àwọn àpẹẹrẹ ńlá tó rọrùn. Ìlà nla, dára fún marker. Olùbẹ̀rẹ̀ àgbàlagbà.', "k": ['ìwé àwọ̀ rọrùn', 'beginner coloring', 'ìlà nla', 'àpẹẹrẹ ńlá', 'àwọ̀ fún àgbà', 'ìwé àwọ̀ àkọ́kọ́', 'marker']},
    },
    "5": {
        "zh": {"t": '简易花园', "s": '47幅粗线大图，简单易涂', "h": '不用浇水的花园。粗线宽容，每页一个大主题，大胆又简单。', "k": ['成人花卉填色', '简易植物填色', '花园填色', '大印花', '植物填色', '放松花卉', '入门花']},
        "hi": {"t": 'आसान बगीचा', "s": '47 बड़े और आसान डिज़ाइन, मोटी लाइनों के साथ', "h": 'ऐसा बगीचा जिसे कभी पानी न देना पड़े। मोटी रेखाएँ, हर पेज एक बड़ा आकार। बोल्ड और आसान।', "k": ['फूल कलरिंग बुक', 'आसान बोटैनिकल', 'गार्डन कलरिंग', 'बड़े फूल', 'पौधे रंगना', 'रिलैक्सिंग फ्लोरल', 'बिगिनर फूल']},
        "es": {"t": 'Jardín fácil', "s": '47 diseños grandes y sencillos con líneas gruesas', "h": 'Un jardín que nunca hay que regar. Líneas gruesas, un gran motivo por página. Fácil y audaz.', "k": ['flores colorear adultos', 'botánico fácil', 'jardín colorear', 'flores grandes', 'plantas colorear', 'floral relajante', 'principiante flores']},
        "fr": {"t": 'Jardin facile', "s": '47 grands motifs faciles aux traits épais', "h": "Un jardin qu'on n'arrose jamais. Traits épais, un grand motif par page. Simple et audacieux.", "k": ['fleurs coloriage adultes', 'botanique facile', 'jardin coloriage', 'grandes fleurs', 'plantes coloriage', 'floral détente', 'débutant fleurs']},
        "ha": {"t": 'Lambu mai sauƙi', "s": 'Zane-zane 47 manyá masu sauƙi da layuka masu kauri', "h": 'Lambu da ba a bushatar ba. Layuka masu kauri, babban zane ɗaya a kowane shafi. Mai sauƙi.', "k": ['furanni launi', 'botanical mai sauƙi', 'lambu launi', 'manyan furanni', 'tsire-tsire launi', 'furanni hutawa', 'beginner furanni']},
        "yo": {"t": 'Ọgbà tó rọrùn', "s": 'Àwọn àpẹẹrẹ ńlá 47 tó rọrùn pẹ̀lú ìlà gbòógì', "h": 'Ọgbà tí a kò ní gbà ní gbogbo ìgbà. Ìlà gbòógì, àpẹẹrẹ ńlá kan lórí ojú-ìwé kọ̀ọ̀kan. Rọrùn.', "k": ['ìwé odòdó', 'botanical rọrùn', 'ọgbà àwọ̀', 'odòdó ńlá', 'ewéko àwọ̀', 'odòdó ìsinmi', 'beginner odòdó']},
    },
    "6": {
        "zh": {"t": '马赛克心智', "s": '57幅彩窗马赛克：镶嵌与伊斯兰星纹', "h": '不难不易刚刚好：像彩窗玻璃一样逐块拼成的马赛克。', "k": ['几何填色', '密铺填色', '马赛克图案', '伊斯兰星', '凯尔特结', '视错觉', '中级几何']},
        "hi": {"t": 'मोज़ेक मन', "s": '57 स्टेंड-ग्लास मोज़ेक, टेसेलेशन और इस्लामी तारे', "h": 'न बहुत आसान न बहुत मुश्किल: स्टेंड-ग्लास की तरह बनते मोज़ेक।', "k": ['ज्यामितीय कलरिंग', 'टेसेलेशन', 'मोज़ेक पैटर्न', 'इस्लामी तारा', 'केल्टिक नॉट', 'ऑप आर्ट', 'इंटरमीडिएट ज्यामिति']},
        "es": {"t": 'Mente mosaico', "s": '57 mosaicos de vitral, teselados y estrellas islámicas', "h": 'El punto justo entre lo fácil y lo difícil: mosaicos que se construyen como un vitral.', "k": ['colorear geométrico', 'teselados', 'mosaico', 'estrella islámica', 'nudo celta', 'op art', 'geometría intermedia']},
        "fr": {"t": 'Esprit mosaïque', "s": '57 mosaïques vitrail, pavages et étoiles islamiques', "h": 'Le juste milieu entre trop facile et trop dur : des mosaïques qui se montent comme un vitrail.', "k": ['coloriage géométrique', 'pavages', 'mosaïque', 'étoile islamique', 'nœud celtique', 'op art', 'géométrie intermédiaire']},
        "ha": {"t": 'Hankalin mosaic', "s": 'Mosaic 57 na gilashin launi, tessellation da taurarin Musulunci', "h": 'Matsakaici tsakanin sauƙi da wahala: mosaic da ke gina kamar gilashin launi.', "k": ['launi lissafi', 'tessellation', 'mosaic', 'tauraron Musulunci', 'Celtic knot', 'op art', 'lissafi matsakaici']},
        "yo": {"t": 'Ọpọlọ mosaic', "s": 'Mósáìkì dídgán àwọ̀ 57, tessellation àti ìràwọ̀ Músùlùmí', "h": 'Aàrin rọrùn àti wàhálà: mósáìkì tí ó ń kọ́ bí dídgán àwọ̀.', "k": ['àwọ̀ jiọ́mẹ́tírì', 'tessellation', 'mosaic', 'ìràwọ̀ Islam', 'Celtic knot', 'op art', 'jiọ́mẹ́tírì àárín']},
    },
    "7": {
        "zh": {"t": '林地奇观', "s": '57幅田园风图案：森林动物、蘑菇与蕨类', "h": '田园森林页。猫头鹰、狐狸、蘑菇、蕨类。中级。', "k": ['林地动物填色', '森林填色', '田园森林', '蘑菇填色', '狐狸猫头鹰', '自然场景', '野生动物填色']},
        "hi": {"t": 'वन आश्चर्य', "s": '57 कॉटेजकोर डिज़ाइन: उल्लू, लोमड़ी, मशरूम और फर्न', "h": 'कॉटेजकोर जंगल पन्ने। उल्लू, लोमड़ी, मशरूम। इंटरमीडिएट।', "k": ['वन्य जीव कलरिंग', 'जंगल कलरिंग', 'कॉटेजकोर वन', 'मशरूम कलरिंग', 'लोमड़ी उल्लू', 'प्रकृति दृश्य', 'वाइल्डलाइफ कलरिंग']},
        "es": {"t": 'Maravillas del bosque', "s": '57 diseños cottagecore: búhos, zorros, setas y helechos', "h": 'Bosque cottagecore. Búhos, zorros, setas, helechos. Intermedio.', "k": ['animales bosque colorear', 'bosque adultos', 'cottagecore bosque', 'setas colorear', 'zorro búho', 'escenas naturaleza', 'vida silvestre']},
        "fr": {"t": 'Merveilles des bois', "s": '57 motifs cottagecore : hiboux, renards, champignons et fougères', "h": 'Forêt cottagecore. Chouettes, renards, champignons. Intermédiaire.', "k": ['animaux forêt coloriage', 'forêt adultes', 'cottagecore forêt', 'champignons', 'renard chouette', 'scènes nature', 'faune']},
        "ha": {"t": 'Abubuwan daji', "s": 'Zane-zane 57 na karkara: dabbokin gida, namisa da ganye', "h": 'Daji na cottagecore. Mujiya, yanyawa, naman kaza. Matsakaici.', "k": ['dabbobin daji launi', 'daji launi', 'cottagecore daji', 'naman kaza', 'yanyawa mujiya', 'yanayi', 'dabbobi daji']},
        "yo": {"t": 'Ìyanu igbó', "s": 'Àwọn àpẹẹrẹ 57 cottagecore: ẹyẹ alẹ́, ẹranko igbó, ẹ̀gbin àti ewé', "h": 'Igbó cottagecore. Òwìwí, kọ̀lọ̀kọ̀lọ̀, olùbẹ. Àárín.', "k": ['ẹranko igbó àwọ̀', 'igbó àwọ̀', 'cottagecore igbó', 'olùbẹ àwọ̀', 'kọ̀lọ̀kọ̀lọ̀ òwìwí', 'àwòrán ìṣẹ́dá', 'ẹranko ìgbẹ́']},
    },
    "8": {
        "zh": {"t": '分形梦', "s": '67个真实分形：谢尔宾斯基、朱利亚集与黄金螺旋', "h": '真分形，不是“灵感几何”。高级细密页。', "k": ['分形填色', '真数学填色', '神圣几何', '高级细密填色', '谢尔宾斯基', '复杂图案', '递归图案']},
        "hi": {"t": 'फ्रैक्टल स्वप्न', "s": '67 असली फ्रैक्टल: सिएरपिंस्की, जूलिया सेट और स्वर्ण सर्पिल', "h": 'असली फ्रैक्टल, सजावटी ज्यामिति नहीं। एडवांस्ड बारीक पन्ने।', "k": ['फ्रैक्टल कलरिंग', 'गणित कलरिंग', 'सेक्रेड ज्यामिति', 'एडवांस्ड कलरिंग', 'सिएरपिन्स्की', 'जटिल पैटर्न', 'रिकर्सिव पैटर्न']},
        "es": {"t": 'Sueños fractales', "s": '67 fractales reales: Sierpinski, conjuntos de Julia y espirales doradas', "h": 'Fractales de verdad, no geometría decorativa. Páginas avanzadas.', "k": ['colorear fractal', 'mates colorear', 'geometría sagrada', 'colorear avanzado', 'sierpinski', 'patrones complejos', 'patrón recursivo']},
        "fr": {"t": 'Rêves fractals', "s": '67 fractales réelles : Sierpinski, ensembles de Julia et spirales dorées', "h": 'Vraies fractales, pas de la géométrie déco. Pages avancées.', "k": ['coloriage fractal', 'maths coloriage', 'géométrie sacrée', 'coloriage avancé', 'sierpinski', 'motifs complexes', 'motif récursif']},
        "ha": {"t": 'Mafarkin fractal', "s": 'Fractals 67 na gaskiya: Sierpinski, Julia da spiral zinariya', "h": 'Fractal na gaske, ba lissafi na ado ba. Shafuka masu wuya.', "k": ['fractal launi', 'lissafi launi', 'sacred geometry', 'launi mai wuya', 'sierpinski', 'complex pattern', 'recursive']},
        "yo": {"t": 'Àlá fractal', "s": 'Fractals 67 òtítọ́: Sierpinski, Julia àti spíráàlì wúrà', "h": 'Fractal gidi, kì í ṣe jiọ́mẹ́tírì ọ̀ṣọ́. Ojú-ìwé tó nira.', "k": ['fractal àwọ̀', 'ìsirò àwọ̀', 'sacred geometry', 'àwọ̀ tó nira', 'sierpinski', 'pattern tó nira', 'recursive']},
    },
    "9": {
        "zh": {"t": '建筑幻象', "s": '67幅精细图案：大教堂、城市景观与玫瑰窗', "h": '哥特、彩窗、城市天际线。高级建筑页。', "k": ['建筑填色', '大教堂填色', '城市细密填色', '彩窗填色', '建筑成人填色', '哥特建筑', '复杂城市']},
        "hi": {"t": 'वास्तुकला दृश्य', "s": '67 जटिल डिज़ाइन: कैथेड्रल, शहर और गुलाब खिड़कियाँ', "h": 'गॉथिक, स्टेन्ड ग्लास, शहर की रेखाएँ। एडवांस्ड आर्किटेक्चर।', "k": ['आर्किटेक्चर कलरिंग', 'कैथेड्रल कलरिंग', 'सिटीस्केप डिटेल्ड', 'स्टेन्ड ग्लास', 'बिल्डिंग कलरिंग', 'गॉथिक आर्किटेक्चर', 'जटिल शहर']},
        "es": {"t": 'Visiones arquitectónicas', "s": '67 diseños intrincados: catedrales, paisajes urbanos y rosetones', "h": 'Gótico, vitrales, skyline. Arquitectura avanzada.', "k": ['arquitectura colorear', 'catedral colorear', 'cityscape detallado', 'vitrales', 'edificios adultos', 'gótico', 'ciudad compleja']},
        "fr": {"t": 'Visions d’architecture', "s": '67 motifs complexes : cathédrales, paysages urbains et rosaces', "h": 'Gothique, vitraux, skyline. Architecture avancée.', "k": ['architecture coloriage', 'cathédrale', 'cityscape détaillé', 'vitraux', 'bâtiments adultes', 'gothique', 'ville complexe']},
        "ha": {"t": 'Hangar gine-gine', "s": 'Zane-zane 67 masu wahala: coci manya, birane da tagogin fure', "h": 'Gothic, stained glass, skyline. Gine-gine masu wuya.', "k": ['gine-gine launi', 'cathedral', 'birni daki-daki', 'stained glass', 'building coloring', 'gothic', 'birni mai wuya']},
        "yo": {"t": 'Ìran ayàwòrán ilé', "s": 'Àwọn àpẹẹrẹ 67 pẹ̀lú ìṣẹ̀dá: ilé ìjọsìn ńlá, ìlú àti fèrèsé àlàáfíà', "h": 'Gothic, stained glass, skyline. Ayàwòrán ilé tó nira.', "k": ['ayàwòrán ilé àwọ̀', 'cathedral', 'ìlú àlàyé', 'stained glass', 'ilé àwọ̀', 'gothic', 'ìlú tó nira']},
    },
    "10": {
        "zh": {"t": '安顿', "s": '每日身体记录，无方案、无打卡，无日期', "h": '每日身体记录。没有多迷走神经操，没有疗程。只记下身体此刻如何。', "k": ['身体日记无日期', '焦虑接地日记', '神经系统日记', '身体扫描笔记本', 'Settle日记', '创伤知情日记', '调节记录']},
        "hi": {"t": 'सेटल', "s": 'रोज़ाना बॉडी ट्रैकिंग, कोई प्रोटोकॉल नहीं, कोई स्ट्रीक नहीं, बिना तारीख', "h": 'रोज़ शरीर का ट्रैक। कोई पॉलीवैगल व्यायाम नहीं। सिर्फ़ अभी शरीर कैसा है।', "k": ['सोमैटिक जर्नल', 'ग्राउंडिंग जर्नल', 'नर्वस सिस्टम जर्नल', 'बॉडी स्कैन', 'settle journal', 'ट्रॉमा इन्फॉर्म्ड', 'रेगुलेशन ट्रैकिंग']},
        "es": {"t": 'Settle', "s": 'Registro diario del cuerpo, sin protocolo ni rachas, sin fechas', "h": 'Registro diario del cuerpo. Sin ejercicios polivagales. Solo cómo está el cuerpo ahora.', "k": ['diario somático', 'diario grounding', 'diario sistema nervioso', 'body scan', 'settle journal', 'trauma informed', 'registro regulación']},
        "fr": {"t": 'Settle', "s": 'Suivi quotidien du corps, sans protocole ni séries, non daté', "h": 'Suivi quotidien du corps. Pas d’exercices polyvagaux. Juste comment le corps est là, maintenant.', "k": ['journal somatique', 'journal grounding', 'journal système nerveux', 'body scan', 'settle journal', 'trauma informed', 'suivi régulation']},
        "ha": {"t": 'Settle', "s": 'Bibiyar jiki ta yau da kullum, ba tsari ba, babu sarkar kwanaki, babu kwanan wata', "h": 'Rajistan jiki kullum. Babu motsa jiki na polyvagal. Yadda jiki yake yanzu kawai.', "k": ['somatic journal', 'grounding journal', 'nervous system', 'body scan', 'settle journal', 'trauma informed', 'regulation']},
        "yo": {"t": 'Settle', "s": 'Ìtọ́ka ara lójoojúmọ́, láìní ètò, láìní ṣíísí, láìsí ọjọ́', "h": 'Ìtọpinpin ara lojoojúmọ́. Kò sí èròjá polyvagal. Bí ara ṣe rí nísinsin yìí nikan.', "k": ['somatic journal', 'grounding journal', 'nervous system', 'body scan', 'settle journal', 'trauma informed', 'regulation']},
    },
    "11": {
        "zh": {"t": '中间季节', "s": '潮热、睡眠、脑雾与就诊记录，无日期', "h": '潮热、盗汗、睡眠、脑雾的记录本。给就诊用，不是疗程。', "k": ['围绝经期日记', '围绝经期症状', '潮热记录', '盗汗记录', '中年激素日记', '脑雾日记', '更年期过渡']},
        "hi": {"t": 'बीच का मौसम', "s": 'हॉट फ्लैश, नींद, ब्रेन फॉग और क्लिनिक नोट्स, बिना तारीख', "h": 'हॉट फ्लैश, नाइट स्वेट, नींद, ब्रेन फॉग का लॉग। क्लिनिक नोट्स, प्रोटोकॉल नहीं।', "k": ['पेरिमेनोपॉज़ जर्नल', 'लक्षण ट्रैकर', 'हॉट फ्लैश लॉग', 'नाइट स्वेट', 'मिडलाइफ़ जर्नल', 'ब्रेन फॉग', 'मेनोपॉज़ ट्रांज़िशन']},
        "es": {"t": 'La estación de en medio', "s": 'Sofocos, sueño, niebla mental y notas clínicas, sin fechas', "h": 'Registro de sofocos, sudores, sueño y niebla mental. Para la consulta, no un protocolo.', "k": ['diario perimenopausia', 'síntomas perimenopausia', 'sofocos registro', 'sudores nocturnos', 'diario mitad de vida', 'niebla mental', 'transición menopausia']},
        "fr": {"t": 'La saison du milieu', "s": 'Bouffées de chaleur, sommeil, brouillard cérébral et notes médicales, non daté', "h": 'Suivi des bouffées, sueurs, sommeil, brouillard. Pour le rendez-vous, pas un protocole.', "k": ['journal périménopause', 'symptômes périménopause', 'bouffées de chaleur', 'sueurs nocturnes', 'journal mi-vie', 'brouillard mental', 'transition ménopause']},
        "ha": {"t": 'Lokacin tsakiya', "s": 'Ɓarnar zafi, barci, hazo a kwakwalwa da rubutun asibiti, babu kwanan wata', "h": 'Rajistan zafi, gumi, barci, hazo. Don asibiti, ba tsarin magani ba.', "k": ['perimenopause journal', 'alamomi', 'hot flash', 'night sweats', 'midlife journal', 'brain fog', 'menopause']},
        "yo": {"t": 'Àkókò àárín', "s": 'Óórùn tó ń gbóná, orun, ìkùukù ọpọlọ àti àkọsílẹ̀ kílíníìkì, láìsí ọjọ́', "h": 'Ìtọpinpin ooru, ògìrì, oorun, ìkùukù. Fún klinik, kì í ṣe ìlànà.', "k": ['perimenopause journal', 'ààmì àìsàn', 'hot flash', 'night sweats', 'midlife journal', 'brain fog', 'menopause']},
    },
    "12": {
        "zh": {"t": '多巴胺菜单', "s": '五道菜加每日点单页，共150页', "h": '把调节刺激变成你经营的餐厅。五道菜：前菜、主菜、配菜、特供、甜点，再每日点单。', "k": ['多巴胺菜单日记', '成人ADHD日记', '多巴胺菜单模板', '执行功能日记', '神经多样日常', 'ADHD刺激记录', 'ADHD动机笔记本']},
        "hi": {"t": 'डोपामाइन मेनू', "s": 'पाँच कोर्स और रोज़ का ऑर्डर टिकट, 150 पेज', "h": 'स्टिमुलेशन को रेस्टोरेंट बनाएँ। पाँच कोर्स, फिर रोज़ ऑर्डर।', "k": ['डोपामाइन मेनू जर्नल', 'ADHD जर्नल', 'डोपामाइन टेम्पलेट', 'एग्ज़िक्यूटिव फंक्शन', 'न्यूरोडाइवर्जेंट', 'ADHD स्टिमुलेशन', 'ADHD मोटिवेशन']},
        "es": {"t": 'El menú de dopamina', "s": 'Cinco platos y un ticket de pedido diario, 150 páginas', "h": 'Convierte regular el estímulo en un restaurante. Cinco platos, luego el ticket diario.', "k": ['diario menú dopamina', 'diario TDAH adultos', 'plantilla dopamine menu', 'función ejecutiva', 'neurodivergente', 'estimulación TDAH', 'motivación TDAH']},
        "fr": {"t": 'Le menu dopamine', "s": 'Cinq plats et un ticket de commande quotidien, 150 pages', "h": 'Réguler la stimulation comme un resto. Cinq plats, puis le ticket du jour.', "k": ['journal menu dopamine', 'journal TDAH adultes', 'modèle dopamine menu', 'fonctions exécutives', 'neurodivergent', 'stimulation TDAH', 'motivation TDAH']},
        "ha": {"t": 'Menu na dopamine', "s": 'Kwas 5 da tikiti na yau da kullum, shafi 150', "h": "Mai da daidaita motsin hankali kamar gidan cin abinci. Kayan cin biyar, sa'an nan oda kullum.", "k": ['dopamine menu journal', 'ADHD journal', 'dopamine template', 'executive function', 'neurodivergent', 'ADHD stimulation', 'ADHD motivation']},
        "yo": {"t": 'Méènù dopamine', "s": 'Oúnjẹ márùn-ún àti tíìkì ìbéwèé ojoojúmọ́, ojú-ìwé 150', "h": 'Ṣe ìṣàkóso ìwúrí bí ilé-oúnjẹ. Ìpín márùn-ún, lẹ́yìn náà òṣìṣẹ́ ojoojúmọ́.', "k": ['dopamine menu journal', 'ADHD journal', 'dopamine template', 'executive function', 'neurodivergent', 'ADHD stimulation', 'ADHD motivation']},
    },
    "13": {
        "zh": {"t": '慢页', "s": '四季慢活：每天一页，不赶时间', "h": '一天一页，不赶。四季、hygge、故意慢。', "k": ['慢生活日记', '季节生活', 'hygge日记', '有意生活', '四季日记', '不赶的晨页', '安静生活']},
        "hi": {"t": 'धीमा पन्ना', "s": 'चार मौसमों के लिए: हर दिन एक ठहराता हुआ पेज', "h": 'दिन में एक पन्ना, बिना जल्दबाज़ी। चार मौसम, ह्यूग।', "k": ['स्लो लिविंग जर्नल', 'सीज़नल लिविंग', 'hygge जर्नल', 'इंटेंशनल लिविंग', 'चार सीज़न', 'अनहरीड मॉर्निंग पेज', 'शांत जीवन']},
        "es": {"t": 'La página lenta', "s": 'Una página tranquila al día para las cuatro estaciones', "h": 'Una página al día, sin prisa. Cuatro estaciones, hygge.', "k": ['diario slow living', 'vida estacional', 'diario hygge', 'vida intencional', 'cuatro estaciones', 'páginas lentas', 'vida quieta']},
        "fr": {"t": 'La page lente', "s": 'Une page sans hâte par jour, aux quatre saisons', "h": 'Une page par jour, sans courir. Quatre saisons, hygge.', "k": ['journal slow living', 'vie saisonnière', 'journal hygge', 'vie intentionnelle', 'quatre saisons', 'pages lentes', 'vie calme']},
        "ha": {"t": 'Shafin jinkiri', "s": 'Shafi ɗaya ba a gaggauta ba a kowace rana, yanayi huɗu', "h": 'Shafi ɗaya a rana, ba gaggawa. Yanayi huɗu, hygge.', "k": ['slow living journal', 'seasonal living', 'hygge journal', 'intentional living', 'yanayi hudu', 'morning pages', 'rayuwa mai natsuwa']},
        "yo": {"t": 'Ojú-ìwé díẹ̀díẹ̀', "s": 'Ojú-ìwé kan láìsí ìsára ojoojúmọ́ fún àwọn àkókò igba mẹ́rin', "h": 'Ojú-ìwé kan lójoojúmọ́, láìsáré. Ìgbà mẹ́rin, hygge.', "k": ['slow living journal', 'seasonal living', 'hygge journal', 'intentional living', 'ìgbà mẹ́rin', 'morning pages', 'ìgbésí ayé rọ́rùn']},
    },
    "14": {
        "zh": {"t": '75 Soft 日记', "s": '更温和的75天挑战记录，含第76天', "h": '温和习惯追踪：75天小目标，每周复盘，不设惩罚。第76天温柔收尾。', "k": ['75 soft日记', '75天温和挑战', '75 soft追踪', '温和习惯', '温和健身日记', '75天健康', 'soft挑战']},
        "hi": {"t": '75 सॉफ्ट जर्नल', "s": 'अधिक कोमल 75-दिन चैलेंज ट्रैकर, दिन 76 शामिल', "h": 'कोमल आदत ट्रैकर: 75 दिन के छोटे लक्ष्य, साप्ताहिक समीक्षा, कोई सज़ा नहीं। दिन 76 शामिल।', "k": ['75 soft जर्नल', '75 दिन जेंटल', '75 soft ट्रैकर', 'कोमल आदत', 'जेंटल फिटनेस', '75 दिन वेलनेस', 'सॉफ्ट चैलेंज']},
        "es": {"t": 'El diario 75 Soft', "s": 'Un seguimiento más amable de 75 días, con página del día 76', "h": 'Hábitos suaves: 75 días de metas pequeñas, repaso semanal, sin castigos. El día 76 está dentro.', "k": ['diario 75 soft', 'reto 75 días suave', 'tracker 75 soft', 'hábito amable', 'fitness amable', '75 días wellness', 'desafío soft']},
        "fr": {"t": 'Le journal 75 Soft', "s": 'Un suivi plus doux de 75 jours, avec la page du jour 76', "h": 'Habitudes en douceur : 75 jours de petits objectifs, bilan hebdomadaire, aucune punition. Le jour 76 est là.', "k": ['journal 75 soft', 'défi 75 jours doux', 'tracker 75 soft', 'habitude douce', 'fitness doux', '75 jours wellness', 'défi soft']},
        "ha": {"t": 'Diary 75 Soft', "s": 'Bibiyar ƙalubale mai laushi na kwana 75, da shafin rana 76', "h": 'Bibi masu taushi: kwanaki 75 na ƙananan manufoyi, bitar mako-mako, ba hukunci ba. Rana 76 tana ciki.', "k": ['75 soft journal', '75 days gentle', '75 soft tracker', 'habit taushi', 'fitness taushi', '75 days wellness', 'soft challenge']},
        "yo": {"t": 'Ìwé 75 Soft', "s": 'Ìtọ́ka ìdíwọ̀ rọrùn ti ọjọ́ 75, pẹ̀lú ojú-ìwé ọjọ́ 76', "h": 'Ìtọpinpin àṣà rọrùn: ọjọ́ 75 ti èté kékeré, ìṣàyẹ̀wò ọ̀sẹ̀, láìsí ìyà. Ọjọ́ 76 wà.', "k": ['75 soft journal', '75 ọjọ́ rọ̀', '75 soft tracker', 'àṣà rọ̀', 'fitness rọ̀', '75 ọjọ́ wellness', 'soft challenge']},
    },
    "15": {
        "zh": {"t": '舒适角落', "s": '49个温馨角落：阅读角、雨窗与舒适房间', "h": '壁炉、雨窗、阅读角落。轻松室内页。', "k": ['舒适填色成人', '舒适空间填色', 'hygge填色', '阅读角落', '田园室内', '壁炉填色', '氛围舒适填色']},
        "hi": {"t": 'आरामदेह कोने', "s": '49 आरामदायक जगहें: रीडिंग नुक, बरसाती खिड़कियाँ, ह्यूगे कमरे', "h": 'फायरप्लेस, बारिश की खिड़की, रीडिंग नुक्कड़। आसान इंटीरियर पन्ने।', "k": ['कोज़ी कलरिंग', 'कोज़ी स्पेस', 'hygge कलरिंग', 'रीडिंग नुक', 'कॉटेजकोर इंटीरियर', 'फायरप्लेस कलरिंग', 'आरामदेह कलरिंग']},
        "es": {"t": 'Rincones acogedores', "s": '49 rincones acogedores: rincones de lectura, ventanas de lluvia y salas hygge', "h": 'Chimenea, lluvia en el cristal, rincón de lectura. Interiores fáciles.', "k": ['colorear cozy adultos', 'espacios cozy', 'colorear hygge', 'rincón lectura', 'interiores cottagecore', 'chimenea colorear', 'colorear acogedor']},
        "fr": {"t": 'Coins douillets', "s": '49 coins cosy : coins lecture, fenêtres de pluie et pièces hygge', "h": 'Cheminée, pluie sur la vitre, coin lecture. Intérieurs faciles.', "k": ['coloriage cozy adultes', 'espaces cozy', 'coloriage hygge', 'coin lecture', 'intérieurs cottagecore', 'cheminée coloriage', 'coloriage douillet']},
        "ha": {"t": 'Kusurwoyi masu nutsuwa', "s": 'Kusurai 49 masu natsuwa: kusurin karatu, tagogin ruwan sama da dakuna', "h": 'Murhu, ruwan sama a taga, wurin karatu. Shafuka masu sauƙi.', "k": ['cozy coloring', 'cozy spaces', 'hygge coloring', 'wurin karatu', 'cottagecore', 'murhu launi', 'launi mai nutsuwa']},
        "yo": {"t": 'Ìgún tó dùn', "s": 'Ààyè 49 tí ó túrà: ipò kíkà, fèrèsé ojò àti yàrá hygge', "h": 'Iná ìdílé, òjò lórí fèrèsé, ìgún ìkàwé. Inú ilé rọrùn.', "k": ['cozy coloring', 'cozy spaces', 'hygge coloring', 'ìgún ìkàwé', 'cottagecore', 'iná ìdílé àwọ̀', 'àwọ̀ tó dùn']},
    },
    "16": {
        "zh": {"t": '植物墨线', "s": '49幅标本图，含真实叶序螺旋', "h": '细线植物。标本板、蕨、真实叶序。细线级。', "k": ['成人植物填色', '细线花卉', '标本填色', '复古植物线描', '细花填色', '蕨与叶', '植物爱好者填色']},
        "hi": {"t": 'वनस्पति स्याही', "s": '49 हर्बेरियम प्लेट, असली फिलोटैक्सिस सर्पिल के साथ', "h": 'फाइन-लाइन पौधे। हर्बेरियम, फर्न, असली पत्ती क्रम।', "k": ['बोटैनिकल कलरिंग', 'फाइन लाइन फ्लोरल', 'हर्बेरियम कलरिंग', 'विंटेज बोटैनिकल', 'डिटेल्ड फूल', 'फर्न पत्ती', 'प्लांट लवर कलरिंग']},
        "es": {"t": 'Tinta botánica', "s": '49 láminas de herbario con espirales de filotaxis reales', "h": 'Plantas en línea fina. Herbario, helechos, filotaxis real.', "k": ['botánico colorear adultos', 'floral línea fina', 'herbario colorear', 'botánico vintage', 'flores detalladas', 'helechos', 'plantas colorear']},
        "fr": {"t": 'Encre botanique', "s": "49 planches d'herbier avec spirales de phyllotaxis réelles", "h": 'Plantes en trait fin. Herbier, fougères, vraie phyllotaxie.', "k": ['botanique coloriage adultes', 'floral trait fin', 'herbier coloriage', 'botanique vintage', 'fleurs détaillées', 'fougères', 'plantes coloriage']},
        "ha": {"t": 'Tawadar tsire-tsire', "s": 'Faranti 49 na tsire-tsire da spiral na gaskiya', "h": 'Tsire-tsire masu sirri. Herbarium, ganye, phyllotaxis.', "k": ['botanical coloring', 'fine line floral', 'herbarium', 'vintage botanical', 'furanni daki-daki', 'ferns', 'plant lover']},
        "yo": {"t": 'Tádà ewéko', "s": 'Àwọn pléètì 49 ti ẹ̀wé pẹ̀lú spíráàlì òtítọ́', "h": 'Ewéko ìlà tẹ́ẹ́rẹ́. Herbarium, ewé àgbònbò, phyllotaxis gidi.', "k": ['botanical coloring', 'fine line floral', 'herbarium', 'vintage botanical', 'odòdó àlàyé', 'ferns', 'plant lover']},
    },
    "17": {
        "zh": {"t": '星图册', "s": '49幅星座图，来自真实星位', "h": '真实星图，不是随意星空涂鸦。月相、夜空、细线。', "k": ['星座填色', '成人星空填色', '真实星图', '月相填色', '天文填色', '细线星系', '夜空填色']},
        "hi": {"t": 'आकाशीय एटलस', "s": '49 नक्षत्र प्लेट, असली तारों की स्थिति से', "h": 'असली स्टार मैप, काल्पनिक आकाश नहीं। चंद्र कला, रात, फाइन-लाइन।', "k": ['नक्षत्र कलरिंग', 'सेलेस्टियल कलरिंग', 'असली स्टार मैप', 'चंद्र कला', 'एस्ट्रोनॉमी कलरिंग', 'गैलेक्सी फाइन लाइन', 'रात आकाश']},
        "es": {"t": 'Atlas celeste', "s": '49 láminas de constelaciones desde posiciones estelares reales', "h": 'Mapas de estrellas de verdad. Fases lunares, cielo nocturno, línea fina.', "k": ['colorear constelaciones', 'celeste adultos', 'mapa estelar real', 'fases lunares', 'astronomía colorear', 'galaxia línea fina', 'cielo nocturno']},
        "fr": {"t": 'Atlas céleste', "s": "49 planches de constellations d'après de vraies positions d'étoiles", "h": 'Vraies cartes du ciel. Phases de lune, nuit, trait fin.', "k": ['coloriage constellations', 'céleste adultes', 'carte du ciel réelle', 'phases lunaires', 'astronomie coloriage', 'galaxie trait fin', 'ciel nocturne']},
        "ha": {"t": 'Atlas na sama', "s": 'Faranti 49 na tauraro daga matsayin gaskiya', "h": 'Taswirar taurari na gaske. Wata, dare, layi sirri.', "k": ['constellation coloring', 'celestial coloring', 'star map', 'moon phases', 'astronomy coloring', 'galaxy fine line', 'night sky']},
        "yo": {"t": 'Átlás ọ̀run', "s": 'Àwọn pléètì 49 ti ìràwọ̀ láti ipò ìràwọ̀ òtítọ́', "h": 'Máàpù ìràwọ̀ gidi. Oṣùpá, alẹ́, ìlà tẹ́ẹ́rẹ́.', "k": ['constellation coloring', 'celestial coloring', 'star map', 'moon phases', 'astronomy coloring', 'galaxy fine line', 'night sky']},
    },
    "18": {
        "zh": {"t": '潮墨', "s": '49幅细线深海图，源于真实对数螺旋', "h": '水母、鹦鹉螺螺线、深海。细线海洋页。', "k": ['成人水母填色', '海洋填色', '鹦鹉螺螺线', '深海填色', '海洋生物细线', '海岸填色', '水下填色']},
        "hi": {"t": 'ज्वारीय स्याही', "s": '49 फाइन-लाइन गहरे समुद्र के प्लेट, असली लॉगरिदमिक सर्पिल से', "h": 'जेलीफ़िश, नॉटिलस सर्पिल, गहरा समुद्र। फाइन-लाइन महासागर।', "k": ['जेलीफ़िश कलरिंग', 'महासागर कलरिंग', 'नॉटिलस सर्पिल', 'डीप सी कलरिंग', 'समुद्री जीवन', 'कोस्टल कलरिंग', 'अंडरवाटर पेज']},
        "es": {"t": 'Tinta de marea', "s": '49 láminas de fondo marino a línea fina, de espirales logarítmicas reales', "h": 'Medusas, espiral de nautilus, mar profundo. Océano en línea fina.', "k": ['medusas colorear adultos', 'océano colorear', 'espiral nautilus', 'mar profundo', 'vida marina línea fina', 'costero colorear', 'páginas bajo el mar']},
        "fr": {"t": 'Encre de marée', "s": "49 planches abyssales au trait fin, d'après de vraies spirales logarithmiques", "h": 'Méduses, spirale du nautile, grand fond. Océan en trait fin.', "k": ['méduses coloriage adultes', 'océan coloriage', 'spirale nautile', 'grands fonds', 'vie marine trait fin', 'littoral coloriage', 'pages sous-marines']},
        "ha": {"t": 'Tawadar igiyar ruwa', "s": 'Faranti 49 na teku mai zurfi da layuka masu ƙanƙanta, daga spiral na lissafi', "h": 'Jellyfish, nautilus, zurfin teku. Teku mai sirri.', "k": ['jellyfish coloring', 'ocean coloring', 'nautilus spiral', 'deep sea', 'marine life', 'coastal coloring', 'underwater']},
        "yo": {"t": 'Tádà ìgbì', "s": 'Àwọn pléètì 49 ti òkun jinlẹ̀ pẹ̀lú ìlà tẹ́ẹ́rẹ́, láti spíráàlì òtítọ́', "h": 'Jellyfish, nautilus, òkun jíjìn. Òkun ìlà tẹ́ẹ́rẹ́.', "k": ['jellyfish coloring', 'ocean coloring', 'nautilus spiral', 'deep sea', 'marine life', 'coastal coloring', 'underwater']},
    },
}

def copy_for(t: dict, lang: str) -> str:
    n = str(int(t["n_raw"]))
    L = LANGS[lang]
    c = COPY[n][lang]
    series = L["series_c"] if "Color" in t["series"] else L["series_j"]
    kws = "\n".join(f"  {i}. {k}" for i, k in enumerate(c["k"], 1))
    return f"""{L['name']}  ·  {t['n']}  ·  Quiet Mind Press
================================
TITLE
{c['t']}

SUBTITLE
{c['s']}

ENGLISH TITLE (do not put on the cover PDF)
{t['title']}

AUTHOR / IMPRINT (KDP author field stays English)
Quiet Mind Press
{L['imprint']}

SERIES
{series}

LANGUAGE OF THE PDF
English — {L['pdf']}

{L['inside'].upper()}
{c['h']}
{L['undated']}
{t['pages']} pages · {t['trim']} in · {t['paper']} paper · B&W · bleed OFF · matte

KEYWORDS
{kws}

{L['price'].upper()}
${t['digital']:.2f}  (same on every store; tiers set by the owner)

{L['disclaimer']}
"""
