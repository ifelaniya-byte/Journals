#!/usr/bin/env python3
"""
Multilingual one-page PDF generator.

Produces translated versions of the most universal, culture-neutral
bestsellers, so the store can sell internationally.

Languages: Spanish (es), French (fr), German (de), Portuguese (pt),
Italian (it), Dutch (nl) — all Latin-script (the DejaVu font in use renders
these perfectly). CJK / Arabic / Devanagari need additional fonts and can be
added later.

Usage:
    python3 1-page-pdfs/generate_i18n.py

Output:
    1-page-pdfs/i18n/<lang>/<product>_<lang>.pdf
"""

from __future__ import annotations

from pathlib import Path

from generate_pdfs import OnePager

BASE = Path(__file__).resolve().parent
OUT = BASE / "i18n"

LANGS = {
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "pt": "Português",
    "it": "Italiano",
    "nl": "Nederlands",
}

# ---------------------------------------------------------------------------
# Translations. Each language maps product -> {string-key -> value}.
# Lists are used for table headers / checklist items / day names.
# ---------------------------------------------------------------------------
STRINGS = {
    "es": {
        "sales": {
            "title": "Registro de Ventas",
            "subtitle": "Registro diario de pedidos: ventas, comisiones y beneficios",
            "business": "Negocio / vendedor:",
            "order_log": "Registro de pedidos",
            "headers": ["Fecha", "Pedido #", "Artículo / SKU", "Cant.", "Precio", "Comisión", "Envío", "Beneficio", "Pago"],
            "summary": "Resumen del período",
            "summary_body": "Ingresos totales $______      Comisiones totales $______      Beneficio total $______",
            "notes": "Notas",
            "best": "Mejor producto de este período:",
        },
        "budget": {
            "title": "Planificador de Presupuesto",
            "subtitle": "Ingresos, gastos y la regla 50/30/20",
            "field": "Mes: __________    Ingreso neto: $____________",
            "income": "Ingresos",
            "income_body": "Sueldo $______    Ingreso extra $______    Otros $______    TOTAL $______",
            "expenses": "Gastos",
            "headers": ["Categoría", "Presupuesto", "Real", "Diferencia"],
            "cats": ["Vivienda", "Comestibles", "Transporte", "Servicios", "Seguros", "Pagos de deuda", "Suscripciones", "Ocio / comidas", "Ahorro", "Otros"],
            "rule": "La regla 50/30/20",
            "rule_body": "50% necesidades · 30% deseos · 20% ahorro / deuda. Mi reparto: ___% / ___% / ___%",
            "goal": "Meta de ahorro",
            "goal_body": "Este mes ahorro $______ para: ________________________",
        },
        "habit": {
            "title": "Registro de Hábitos",
            "subtitle": "Cuadrícula de cinco semanas con rachas",
            "field": "Mes: __________    Hábito principal: ________________________",
            "grid": "Cuadrícula semanal (marca X o ✓ por día)",
            "headers": ["Hábito", "Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Racha"],
            "why": "Motivación y recompensa",
            "why_body": "Por qué importa: ____________________________________________________",
            "reward": "Recompensa a los 7 días: ________________    Recompensa a los 30 días: ________________",
        },
        "meal": {
            "title": "Planificador de Comidas y Compras",
            "subtitle": "Planifica la semana y compra una sola vez",
            "field": "Semana del: __________",
            "meals": "Comidas",
            "headers": ["Día", "Desayuno", "Almuerzo", "Cena", "Meriendas"],
            "days": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
            "grocery": "Lista de compras",
        },
        "password": {
            "title": "Registro de Contraseñas",
            "subtitle": "Todas tus cuentas en un lugar seguro",
            "muted": "Mantén esta página privada. Considera un gestor de contraseñas.",
            "accounts": "Cuentas",
            "headers": ["Sitio / App", "Usuario", "Correo", "Contraseña", "Pregunta seg.", "Notas"],
            "updates": "Actualizaciones",
            "updates_body": "Contraseña cambiada: ________    Última revisión: ________    Verificación en dos pasos: ☐",
        },
        "packing": {
            "title": "Lista de Equipaje",
            "subtitle": "Empaca por categoría y no olvides nada",
            "field": "Viaje: ______________________    Fechas: ___/___/___  →  ___/___/___",
            "clothing": "Ropa",
            "clothing_items": ["Ropa interior", "Calcetines", "Camisetas", "Pantalones", "Suéter / chaqueta", "Pijama", "Zapatos", "Traje de baño"],
            "toiletries": "Artículos de aseo",
            "toiletries_items": ["Cepillo / pasta dental", "Desodorante", "Champú / jabón", "Cuidado de la piel", "Medicamentos", "Rasuradora"],
            "tech": "Tecnología y documentos",
            "tech_items": ["Teléfono + cargador", "Batería externa", "Adaptador", "ID / pasaporte", "Boletos", "Cartera / tarjetas", "Llaves"],
            "last": "Verificación final",
            "last_items": ["Snacks", "Botella de agua", "Audífonos", "Libro", "Paraguas", "Bolsa reutilizable"],
        },
        "goal": {
            "title": "Planificador de Metas SMART",
            "subtitle": "Convierte una meta en un plan que cumplirás",
            "field": "Meta: ________________________________________________________________",
            "smart": "Hazla SMART",
            "s": "S — Específica (¿qué exactamente?):",
            "m": "M — Medible (¿cómo lo sabrás?):",
            "a": "A — Alcanzable (¿es realista?):",
            "r": "R — Relevante (¿por qué ahora?):",
            "t": "T — Con límite de tiempo (¿para cuándo?):",
            "actions": "Pasos de acción",
            "a1": "1. Primer paso (próximas 24 h):",
            "a2": "2. Esta semana:",
            "a3": "3. Este mes:",
            "milestones": "Hitos y revisión",
            "m1": "Hito 1 (para ______): ______________    Hito 2 (para ______): ______________",
        },
        "workout": {
            "title": "Registro de Entrenamiento",
            "subtitle": "Ejercicios, series, repeticiones y progreso",
            "field": "Meta: ______________________    Semana del: __________",
            "workouts": "Entrenamientos",
            "headers": ["Día", "Ejercicio", "Series × Reps", "Peso", "Notas"],
            "progress": "Progreso",
            "progress_body": "Esta semana: Peso ______    Cardio ______ min    Récords: ____________________",
        },
    },
    "fr": {
        "sales": {
            "title": "Registre des Ventes",
            "subtitle": "Journal quotidien : ventes, frais et bénéfices",
            "business": "Entreprise / vendeur :",
            "order_log": "Journal des commandes",
            "headers": ["Date", "Cmd #", "Article / SKU", "Qté", "Prix", "Frais", "Livr.", "Bénéfice", "Paiem."],
            "summary": "Résumé de la période",
            "summary_body": "Revenus totaux $______      Frais totaux $______      Bénéfice total $______",
            "notes": "Notes",
            "best": "Meilleure vente de la période :",
        },
        "budget": {
            "title": "Planificateur de Budget",
            "subtitle": "Revenus, dépenses et la règle 50/30/20",
            "field": "Mois : __________    Revenu net : $____________",
            "income": "Revenus",
            "income_body": "Salaire $______    Revenu d'appoint $______    Autre $______    TOTAL $______",
            "expenses": "Dépenses",
            "headers": ["Catégorie", "Budget", "Réel", "Écart"],
            "cats": ["Logement", "Alimentation", "Transport", "Factures", "Assurances", "Remboursement de dettes", "Abonnements", "Loisirs / sorties", "Épargne", "Autre"],
            "rule": "La règle 50/30/20",
            "rule_body": "50 % besoins · 30 % envies · 20 % épargne / dettes. Ma répartition : ___% / ___% / ___%",
            "goal": "Objectif d'épargne",
            "goal_body": "Ce mois-ci j'épargne $______ pour : ________________________",
        },
        "habit": {
            "title": "Suivi d'Habitudes",
            "subtitle": "Grille de cinq semaines avec séries",
            "field": "Mois : __________    Habitude prioritaire : ________________________",
            "grid": "Grille hebdomadaire (cochez X ou ✓ par jour)",
            "headers": ["Habitude", "Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Série"],
            "why": "Motivation et récompense",
            "why_body": "Pourquoi c'est important : ____________________________________________________",
            "reward": "Récompense à 7 jours : ________________    Récompense à 30 jours : ________________",
        },
        "meal": {
            "title": "Planificateur de Repas et de Courses",
            "subtitle": "Planifiez la semaine, faites les courses une fois",
            "field": "Semaine du : __________",
            "meals": "Repas",
            "headers": ["Jour", "Petit-déj.", "Déjeuner", "Dîner", "Collations"],
            "days": ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"],
            "grocery": "Liste de courses",
        },
        "password": {
            "title": "Registre des Mots de Passe",
            "subtitle": "Tous vos identifiants en un lieu sûr",
            "muted": "Gardez cette page privée. Pensez à un gestionnaire de mots de passe.",
            "accounts": "Comptes",
            "headers": ["Site / App", "Identifiant", "E-mail", "Mot de passe", "Question sécu.", "Notes"],
            "updates": "Mises à jour",
            "updates_body": "Mot de passe changé : ________    Dernière révision : ________    Double authentification : ☐",
        },
        "packing": {
            "title": "Liste de Bagages",
            "subtitle": "Faites vos bagages par catégorie, sans rien oublier",
            "field": "Voyage : ______________________    Dates : ___/___/___  →  ___/___/___",
            "clothing": "Vêtements",
            "clothing_items": ["Sous-vêtements", "Chaussettes", "T-shirts", "Pantalons", "Pull / veste", "Pyjama", "Chaussures", "Maillot de bain"],
            "toiletries": "Articles de toilette",
            "toiletries_items": ["Brosse / dentifrice", "Déodorant", "Shampoing / savon", "Soins de la peau", "Médicaments", "Rasoir"],
            "tech": "Technologie et documents",
            "tech_items": ["Téléphone + chargeur", "Batterie externe", "Adaptateur", "Carte d'identité / passeport", "Billets", "Portefeuille / cartes", "Clés"],
            "last": "Dernière vérification",
            "last_items": ["En-cas", "Bouteille d'eau", "Écouteurs", "Livre", "Parapluie", "Sac réutilisable"],
        },
        "goal": {
            "title": "Planificateur d'Objectifs SMART",
            "subtitle": "Transformez un objectif en plan réalisable",
            "field": "Objectif : ________________________________________________________________",
            "smart": "Rendez-le SMART",
            "s": "S — Spécifique (quoi exactement ?) :",
            "m": "M — Mesurable (comment le saurez-vous ?) :",
            "a": "A — Atteignable (est-ce réaliste ?) :",
            "r": "R — Pertinent (pourquoi maintenant ?) :",
            "t": "T — Temporel (pour quand ?) :",
            "actions": "Étapes d'action",
            "a1": "1. Première étape (prochaines 24 h) :",
            "a2": "2. Cette semaine :",
            "a3": "3. Ce mois-ci :",
            "milestones": "Jalons et révision",
            "m1": "Jalon 1 (avant ______) : ______________    Jalon 2 (avant ______) : ______________",
        },
        "workout": {
            "title": "Journal d'Entraînement",
            "subtitle": "Exercices, séries, répétitions et progrès",
            "field": "Objectif : ______________________    Semaine du : __________",
            "workouts": "Entraînements",
            "headers": ["Jour", "Exercice", "Séries × Rép.", "Poids", "Notes"],
            "progress": "Progrès",
            "progress_body": "Cette semaine : Poids ______    Cardio ______ min    Records : ____________________",
        },
    },
    "de": {
        "sales": {
            "title": "Verkaufs-Tracker",
            "subtitle": "Tägliches Bestellprotokoll: Verkäufe, Gebühren und Gewinn",
            "business": "Geschäft / Verkäufer:",
            "order_log": "Bestellprotokoll",
            "headers": ["Datum", "Bestell-Nr.", "Artikel / SKU", "Menge", "Preis", "Gebühren", "Versand", "Gewinn", "Zahlung"],
            "summary": "Zusammenfassung",
            "summary_body": "Gesamtumsatz $______      Gesamtgebühren $______      Gesamtgewinn $______",
            "notes": "Notizen",
            "best": "Bester Artikel dieser Periode:",
        },
        "budget": {
            "title": "Budget-Planer",
            "subtitle": "Einnahmen, Ausgaben und die 50/30/20-Regel",
            "field": "Monat: __________    Nettoeinkommen: $____________",
            "income": "Einnahmen",
            "income_body": "Gehalt $______    Nebeneinkünfte $______    Sonstiges $______    GESAMT $______",
            "expenses": "Ausgaben",
            "headers": ["Kategorie", "Budget", "Ist", "Differenz"],
            "cats": ["Wohnen", "Lebensmittel", "Transport", "Nebenkosten", "Versicherungen", "Schulden", "Abonnements", "Freizeit / Essen", "Sparen", "Sonstiges"],
            "rule": "Die 50/30/20-Regel",
            "rule_body": "50 % Bedürfnisse · 30 % Wünsche · 20 % Sparen / Schulden. Meine Aufteilung: ___% / ___% / ___%",
            "goal": "Sparziel",
            "goal_body": "Diesen Monat spare ich $______ für: ________________________",
        },
        "habit": {
            "title": "Gewohnheits-Tracker",
            "subtitle": "Fünf-Wochen-Raster mit Serien",
            "field": "Monat: __________    Fokus-Gewohnheit: ________________________",
            "grid": "Wochenraster (X oder ✓ pro Tag eintragen)",
            "headers": ["Gewohnheit", "Wo 1", "Wo 2", "Wo 3", "Wo 4", "Wo 5", "Serie"],
            "why": "Motivation und Belohnung",
            "why_body": "Warum es wichtig ist: ____________________________________________________",
            "reward": "Belohnung nach 7 Tagen: ________________    Belohnung nach 30 Tagen: ________________",
        },
        "meal": {
            "title": "Essens- und Einkaufsplaner",
            "subtitle": "Die Woche planen, einmal einkaufen",
            "field": "Woche vom: __________",
            "meals": "Mahlzeiten",
            "headers": ["Tag", "Frühstück", "Mittag", "Abend", "Snacks"],
            "days": ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
            "grocery": "Einkaufsliste",
        },
        "password": {
            "title": "Passwort-Register",
            "subtitle": "Alle Zugangsdaten an einem sicheren Ort",
            "muted": "Diese Seite privat aufbewahren. Ein Passwort-Manager ist empfohlen.",
            "accounts": "Konten",
            "headers": ["Seite / App", "Benutzer", "E-Mail", "Passwort", "Sicherheitsfrage", "Notizen"],
            "updates": "Aktualisierungen",
            "updates_body": "Passwort geändert: ________    Letzte Prüfung: ________    Zwei-Faktor-Authentifizierung: ☐",
        },
        "packing": {
            "title": "Packliste",
            "subtitle": "Nach Kategorien packen, nichts vergessen",
            "field": "Reise: ______________________    Daten: ___/___/___  →  ___/___/___",
            "clothing": "Kleidung",
            "clothing_items": ["Unterwäsche", "Socken", "T-Shirts", "Hosen", "Pullover / Jacke", "Schlafkleidung", "Schuhe", "Badekleidung"],
            "toiletries": "Toilettenartikel",
            "toiletries_items": ["Zahnbürste / Zahnpasta", "Deodorant", "Shampoo / Seife", "Hautpflege", "Medikamente", "Rasierer"],
            "tech": "Technik und Dokumente",
            "tech_items": ["Handy + Ladegerät", "Powerbank", "Adapter", "Ausweis / Reisepass", "Tickets", "Geldbeutel / Karten", "Schlüssel"],
            "last": "Letzter Check",
            "last_items": ["Snacks", "Wasserflasche", "Kopfhörer", "Buch", "Regenschirm", "Mehrwegbeutel"],
        },
        "goal": {
            "title": "SMART-Ziel-Planer",
            "subtitle": "Aus einem Ziel einen umsetzbaren Plan machen",
            "field": "Ziel: ________________________________________________________________",
            "smart": "Mach es SMART",
            "s": "S — Spezifisch (was genau?):",
            "m": "M — Messbar (woran erkennst du es?):",
            "a": "A — Erreichbar (ist es realistisch?):",
            "r": "R — Relevant (warum jetzt?):",
            "t": "T — Terminiert (bis wann?):",
            "actions": "Aktionsschritte",
            "a1": "1. Erster Schritt (nächste 24 Std.):",
            "a2": "2. Diese Woche:",
            "a3": "3. Diesen Monat:",
            "milestones": "Meilensteine und Rückblick",
            "m1": "Meilenstein 1 (bis ______): ______________    Meilenstein 2 (bis ______): ______________",
        },
        "workout": {
            "title": "Trainingsprotokoll",
            "subtitle": "Übungen, Sätze, Wiederholungen und Fortschritt",
            "field": "Ziel: ______________________    Woche vom: __________",
            "workouts": "Workouts",
            "headers": ["Tag", "Übung", "Sätze × Wdh.", "Gewicht", "Notizen"],
            "progress": "Fortschritt",
            "progress_body": "Diese Woche: Gewicht ______    Cardio ______ min    Bestleistungen: ____________________",
        },
    },
    "pt": {
        "sales": {
            "title": "Registro de Vendas",
            "subtitle": "Registro diário de pedidos: vendas, taxas e lucro",
            "business": "Negócio / vendedor:",
            "order_log": "Registro de pedidos",
            "headers": ["Data", "Pedido #", "Item / SKU", "Qtd.", "Preço", "Taxas", "Frete", "Lucro", "Pagto."],
            "summary": "Resumo do período",
            "summary_body": "Receita total $______      Taxas totais $______      Lucro total $______",
            "notes": "Notas",
            "best": "Melhor venda do período:",
        },
        "budget": {
            "title": "Planejador de Orçamento",
            "subtitle": "Receitas, despesas e a regra 50/30/20",
            "field": "Mês: __________    Renda líquida: $____________",
            "income": "Receitas",
            "income_body": "Salário $______    Renda extra $______    Outros $______    TOTAL $______",
            "expenses": "Despesas",
            "headers": ["Categoria", "Orçamento", "Real", "Diferença"],
            "cats": ["Moradia", "Alimentação", "Transporte", "Contas", "Seguros", "Pagamento de dívidas", "Assinaturas", "Lazer / refeições", "Poupança", "Outros"],
            "rule": "A regra 50/30/20",
            "rule_body": "50% necessidades · 30% desejos · 20% poupança / dívidas. Minha divisão: ___% / ___% / ___%",
            "goal": "Meta de poupança",
            "goal_body": "Este mês vou poupar $______ para: ________________________",
        },
        "habit": {
            "title": "Rastreador de Hábitos",
            "subtitle": "Grade de cinco semanas com sequências",
            "field": "Mês: __________    Hábito principal: ________________________",
            "grid": "Grade semanal (marque X ou ✓ por dia)",
            "headers": ["Hábito", "Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sequência"],
            "why": "Motivação e recompensa",
            "why_body": "Por que isso importa: ____________________________________________________",
            "reward": "Recompensa aos 7 dias: ________________    Recompensa aos 30 dias: ________________",
        },
        "meal": {
            "title": "Planejador de Refeições e Compras",
            "subtitle": "Planeje a semana e compre uma vez só",
            "field": "Semana de: __________",
            "meals": "Refeições",
            "headers": ["Dia", "Café da manhã", "Almoço", "Jantar", "Lanches"],
            "days": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
            "grocery": "Lista de compras",
        },
        "password": {
            "title": "Registro de Senhas",
            "subtitle": "Todos os seus acessos em um lugar seguro",
            "muted": "Mantenha esta página privada. Considere um gerenciador de senhas.",
            "accounts": "Contas",
            "headers": ["Site / App", "Usuário", "E-mail", "Senha", "Pergunta de seg.", "Notas"],
            "updates": "Atualizações",
            "updates_body": "Senha alterada: ________    Última revisão: ________    Verificação em duas etapas: ☐",
        },
        "packing": {
            "title": "Lista de Bagagem",
            "subtitle": "Faça as malas por categoria, sem esquecer nada",
            "field": "Viagem: ______________________    Datas: ___/___/___  →  ___/___/___",
            "clothing": "Roupas",
            "clothing_items": ["Roupa íntima", "Meias", "Camisetas", "Calças", "Suéter / casaco", "Pijama", "Sapatos", "Roupa de banho"],
            "toiletries": "Artigos de higiene",
            "toiletries_items": ["Escova / pasta de dente", "Desodorante", "Shampoo / sabonete", "Cuidados com a pele", "Medicamentos", "Lâmina"],
            "tech": "Tecnologia e documentos",
            "tech_items": ["Celular + carregador", "Bateria externa", "Adaptador", "RG / passaporte", "Passagens", "Carteira / cartões", "Chaves"],
            "last": "Verificação final",
            "last_items": ["Lanches", "Garrafa de água", "Fones", "Livro", "Guarda-chuva", "Sacola reutilizável"],
        },
        "goal": {
            "title": "Planejador de Metas SMART",
            "subtitle": "Transforme uma meta em um plano que você vai seguir",
            "field": "Meta: ________________________________________________________________",
            "smart": "Torne-a SMART",
            "s": "S — Específica (o que exatamente?):",
            "m": "M — Mensurável (como vai saber?):",
            "a": "A — Alcançável (é realista?):",
            "r": "R — Relevante (por que agora?):",
            "t": "T — Temporal (até quando?):",
            "actions": "Passos de ação",
            "a1": "1. Primeiro passo (próximas 24 h):",
            "a2": "2. Esta semana:",
            "a3": "3. Este mês:",
            "milestones": "Marcos e revisão",
            "m1": "Marco 1 (até ______): ______________    Marco 2 (até ______): ______________",
        },
        "workout": {
            "title": "Registro de Treino",
            "subtitle": "Exercícios, séries, repetições e progresso",
            "field": "Meta: ______________________    Semana de: __________",
            "workouts": "Treinos",
            "headers": ["Dia", "Exercício", "Séries × Rep.", "Peso", "Notas"],
            "progress": "Progresso",
            "progress_body": "Esta semana: Peso ______    Cardio ______ min    Recordes: ____________________",
        },
    },
    "it": {
        "sales": {
            "title": "Registro Vendite",
            "subtitle": "Registro giornaliero: vendite, commissioni e profitto",
            "business": "Attività / venditore:",
            "order_log": "Registro ordini",
            "headers": ["Data", "Ordine #", "Articolo / SKU", "Qtà", "Prezzo", "Commissioni", "Sped.", "Profitto", "Pag."],
            "summary": "Riepilogo del periodo",
            "summary_body": "Ricavi totali $______      Commissioni totali $______      Profitto totale $______",
            "notes": "Note",
            "best": "Articolo migliore del periodo:",
        },
        "budget": {
            "title": "Pianificatore di Budget",
            "subtitle": "Entrate, uscite e la regola 50/30/20",
            "field": "Mese: __________    Reddito netto: $____________",
            "income": "Entrate",
            "income_body": "Stipendio $______    Entrate extra $______    Altro $______    TOTALE $______",
            "expenses": "Uscite",
            "headers": ["Categoria", "Budget", "Effettivo", "Differenza"],
            "cats": ["Casa", "Spesa alimentare", "Trasporti", "Bollette", "Assicurazioni", "Rimborso debiti", "Abbonamenti", "Svago / pasti fuori", "Risparmio", "Altro"],
            "rule": "La regola 50/30/20",
            "rule_body": "50% necessità · 30% desideri · 20% risparmio / debiti. La mia divisione: ___% / ___% / ___%",
            "goal": "Obiettivo di risparmio",
            "goal_body": "Questo mese risparmio $______ per: ________________________",
        },
        "habit": {
            "title": "Tracciatore di Abitudini",
            "subtitle": "Griglia di cinque settimane con serie",
            "field": "Mese: __________    Abitudine principale: ________________________",
            "grid": "Griglia settimanale (segna X o ✓ per giorno)",
            "headers": ["Abitudine", "Sett 1", "Sett 2", "Sett 3", "Sett 4", "Sett 5", "Serie"],
            "why": "Motivazione e ricompensa",
            "why_body": "Perché è importante: ____________________________________________________",
            "reward": "Ricompensa a 7 giorni: ________________    Ricompensa a 30 giorni: ________________",
        },
        "meal": {
            "title": "Pianificatore Pasti e Spesa",
            "subtitle": "Pianifica la settimana, fai la spesa una volta",
            "field": "Settimana del: __________",
            "meals": "Pasti",
            "headers": ["Giorno", "Colazione", "Pranzo", "Cena", "Spuntini"],
            "days": ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"],
            "grocery": "Lista della spesa",
        },
        "password": {
            "title": "Registro Password",
            "subtitle": "Tutti i tuoi accessi in un luogo sicuro",
            "muted": "Tieni questa pagina privata. Considera un gestore di password.",
            "accounts": "Account",
            "headers": ["Sito / App", "Utente", "Email", "Password", "Domanda di sicurezza", "Note"],
            "updates": "Aggiornamenti",
            "updates_body": "Password cambiata: ________    Ultima revisione: ________    Verifica in due passaggi: ☐",
        },
        "packing": {
            "title": "Lista Valigia",
            "subtitle": "Prepara la valigia per categoria, senza dimenticare nulla",
            "field": "Viaggio: ______________________    Date: ___/___/___  →  ___/___/___",
            "clothing": "Abbigliamento",
            "clothing_items": ["Intimo", "Calzini", "Magliette", "Pantaloni", "Maglione / giacca", "Pigiama", "Scarpe", "Costume"],
            "toiletries": "Articoli da bagno",
            "toiletries_items": ["Spazzolino / dentifricio", "Deodorante", "Shampoo / sapone", "Cura della pelle", "Farmaci", "Rasoio"],
            "tech": "Tecnologia e documenti",
            "tech_items": ["Telefono + caricatore", "Power bank", "Adattatore", "Documento / passaporto", "Biglietti", "Portafoglio / carte", "Chiavi"],
            "last": "Controllo finale",
            "last_items": ["Snack", "Bottiglia d'acqua", "Cuffie", "Libro", "Ombrello", "Borsa riutilizzabile"],
        },
        "goal": {
            "title": "Pianificatore di Obiettivi SMART",
            "subtitle": "Trasforma un obiettivo in un piano che seguirai",
            "field": "Obiettivo: ________________________________________________________________",
            "smart": "Rendilo SMART",
            "s": "S — Specifico (cosa esattamente?):",
            "m": "M — Misurabile (come lo saprai?):",
            "a": "A — Raggiungibile (è realistico?):",
            "r": "R — Rilevante (perché ora?):",
            "t": "T — Temporizzato (entro quando?):",
            "actions": "Passi d'azione",
            "a1": "1. Primo passo (prossime 24 ore):",
            "a2": "2. Questa settimana:",
            "a3": "3. Questo mese:",
            "milestones": "Tappe e revisione",
            "m1": "Tappa 1 (entro ______): ______________    Tappa 2 (entro ______): ______________",
        },
        "workout": {
            "title": "Diario di Allenamento",
            "subtitle": "Esercizi, serie, ripetizioni e progressi",
            "field": "Obiettivo: ______________________    Settimana del: __________",
            "workouts": "Allenamenti",
            "headers": ["Giorno", "Esercizio", "Serie × Rip.", "Peso", "Note"],
            "progress": "Progressi",
            "progress_body": "Questa settimana: Peso ______    Cardio ______ min    Record: ____________________",
        },
    },
    "nl": {
        "sales": {
            "title": "Verkooptracker",
            "subtitle": "Dagelijks orderlogboek: verkopen, kosten en winst",
            "business": "Bedrijf / verkoper:",
            "order_log": "Orderlogboek",
            "headers": ["Datum", "Order #", "Artikel / SKU", "Aantal", "Prijs", "Kosten", "Verz.", "Winst", "Betaling"],
            "summary": "Samenvatting",
            "summary_body": "Totale omzet $______      Totale kosten $______      Totale winst $______",
            "notes": "Notities",
            "best": "Beste verkoper van deze periode:",
        },
        "budget": {
            "title": "Budgetplanner",
            "subtitle": "Inkomsten, uitgaven en de 50/30/20-regel",
            "field": "Maand: __________    Netto-inkomen: $____________",
            "income": "Inkomsten",
            "income_body": "Salaris $______    Extra inkomen $______    Overig $______    TOTAAL $______",
            "expenses": "Uitgaven",
            "headers": ["Categorie", "Budget", "Werkelijk", "Verschil"],
            "cats": ["Wonen", "Boodschappen", "Vervoer", "Vaste lasten", "Verzekeringen", "Schulden aflossen", "Abonnementen", "Uitgaan / eten", "Sparen", "Overig"],
            "rule": "De 50/30/20-regel",
            "rule_body": "50% behoeften · 30% wensen · 20% sparen / schulden. Mijn verdeling: ___% / ___% / ___%",
            "goal": "Spaardoel",
            "goal_body": "Deze maand spaar ik $______ voor: ________________________",
        },
        "habit": {
            "title": "Gewoontetracker",
            "subtitle": "Vijf weken raster met reeksen",
            "field": "Maand: __________    Focus-gewoonte: ________________________",
            "grid": "Weekraster (vul X of ✓ per dag in)",
            "headers": ["Gewoonte", "Wk 1", "Wk 2", "Wk 3", "Wk 4", "Wk 5", "Reeks"],
            "why": "Motivatie en beloning",
            "why_body": "Waarom het belangrijk is: ____________________________________________________",
            "reward": "Beloning na 7 dagen: ________________    Beloning na 30 dagen: ________________",
        },
        "meal": {
            "title": "Maaltijd- en Boodschappenplanner",
            "subtitle": "Plan de week, doe één keer boodschappen",
            "field": "Week van: __________",
            "meals": "Maaltijden",
            "headers": ["Dag", "Ontbijt", "Lunch", "Avondeten", "Snacks"],
            "days": ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"],
            "grocery": "Boodschappenlijst",
        },
        "password": {
            "title": "Wachtwoordenregister",
            "subtitle": "Al je inloggegevens op één veilige plek",
            "muted": "Houd deze pagina privé. Overweeg een wachtwoordmanager.",
            "accounts": "Accounts",
            "headers": ["Site / App", "Gebruiker", "E-mail", "Wachtwoord", "Beveiligingsvraag", "Notities"],
            "updates": "Updates",
            "updates_body": "Wachtwoord gewijzigd: ________    Laatste controle: ________    Twee-stapsverificatie: ☐",
        },
        "packing": {
            "title": "Paklijst",
            "subtitle": "Pak per categorie in, zonder iets te vergeten",
            "field": "Reis: ______________________    Data: ___/___/___  →  ___/___/___",
            "clothing": "Kleding",
            "clothing_items": ["Ondergoed", "Sokken", "T-shirts", "Broeken", "Trui / jas", "Pyjama", "Schoenen", "Zwemkleding"],
            "toiletries": "Toiletartikelen",
            "toiletries_items": ["Tandenborstel / tandpasta", "Deodorant", "Shampoo / zeep", "Huidverzorging", "Medicijnen", "Scheermes"],
            "tech": "Techniek en documenten",
            "tech_items": ["Telefoon + oplader", "Powerbank", "Adapter", "ID / paspoort", "Tickets", "Portemonnee / kaarten", "Sleutels"],
            "last": "Laatste controle",
            "last_items": ["Snacks", "Waterfles", "Koptelefoon", "Boek", "Paraplu", "Herbruikbare tas"],
        },
        "goal": {
            "title": "SMART-doelenplanner",
            "subtitle": "Maak van een doel een plan dat je echt volgt",
            "field": "Doel: ________________________________________________________________",
            "smart": "Maak het SMART",
            "s": "S — Specifiek (wat precies?):",
            "m": "M — Meetbaar (hoe weet je het?):",
            "a": "A — Acceptabel (is het realistisch?):",
            "r": "R — Relevant (waarom nu?):",
            "t": "T — Tijdgebonden (wanneer?):",
            "actions": "Actiestappen",
            "a1": "1. Eerste stap (komende 24 uur):",
            "a2": "2. Deze week:",
            "a3": "3. Deze maand:",
            "milestones": "Mijlpalen en evaluatie",
            "m1": "Mijlpaal 1 (voor ______): ______________    Mijlpaal 2 (voor ______): ______________",
        },
        "workout": {
            "title": "Trainingslogboek",
            "subtitle": "Oefeningen, sets, herhalingen en voortgang",
            "field": "Doel: ______________________    Week van: __________",
            "workouts": "Trainingen",
            "headers": ["Dag", "Oefening", "Sets × Herh.", "Gewicht", "Notities"],
            "progress": "Voortgang",
            "progress_body": "Deze week: Gewicht ______    Cardio ______ min    Records: ____________________",
        },
    },
}


# ---------------------------------------------------------------------------
# Builders — each renders one product from a language's translation dict `t`.
# ---------------------------------------------------------------------------

def build_sales(t, outdir):
    p = OnePager(t["title"], t["subtitle"], (16, 92, 120))
    p.header()
    p.field_row(t["business"] + " ____________________________", lines=1)
    p.section(t["order_log"])
    p.table(t["headers"], [[""] * len(t["headers"]) for _ in range(9)],
            [20, 20, 44, 12, 19, 17, 17, 19, 23.9])
    p.ln(1)
    p.section(t["summary"])
    p.body(t["summary_body"], size=8.6)
    p.ln(1)
    p.section(t["notes"])
    p.field_row(t["best"], lines=1)
    p.footer()
    p.output(str(outdir / "sales.pdf"))


def build_budget(t, outdir):
    p = OnePager(t["title"], t["subtitle"], (20, 100, 80))
    p.header()
    p.field_row(t["field"], lines=1)
    p.section(t["income"])
    p.field_row(t["income_body"], lines=1)
    p.section(t["expenses"])
    rows = [[c, "", "", ""] for c in t["cats"]]
    p.table(t["headers"], rows, [70, 40.6, 40.6, 40.6])
    p.section(t["rule"])
    p.body(t["rule_body"], size=8.4)
    p.section(t["goal"])
    p.field_row(t["goal_body"], lines=1)
    p.footer()
    p.output(str(outdir / "budget.pdf"))


def build_habit(t, outdir):
    p = OnePager(t["title"], t["subtitle"], (40, 120, 140))
    p.header()
    p.field_row(t["field"], lines=1)
    p.section(t["grid"])
    p.table(t["headers"], [[""] * len(t["headers"]) for _ in range(14)],
            [66, 18, 18, 18, 18, 18, 35.9])
    p.section(t["why"])
    p.field_row(t["why_body"], lines=1)
    p.field_row(t["reward"], lines=1)
    p.footer()
    p.output(str(outdir / "habit.pdf"))


def build_meal(t, outdir):
    p = OnePager(t["title"], t["subtitle"], (160, 90, 40))
    p.header()
    p.field_row(t["field"], lines=1)
    p.section(t["meals"])
    rows = [[d, "", "", "", ""] for d in t["days"]]
    p.table(t["headers"], rows, [20, 43, 43, 43, 42.9])
    p.section(t["grocery"])
    p.checklist(["", "", "", "", "", "", "", ""], cols=2)
    p.footer()
    p.output(str(outdir / "meal.pdf"))


def build_password(t, outdir):
    p = OnePager(t["title"], t["subtitle"], (60, 70, 90))
    p.header()
    p.muted(t["muted"])
    p.section(t["accounts"])
    p.table(t["headers"], [[""] * len(t["headers"]) for _ in range(12)],
            [42, 34, 42, 34, 30, 9.9])
    p.section(t["updates"])
    p.body(t["updates_body"], size=8.0)
    p.footer()
    p.output(str(outdir / "password.pdf"))


def build_packing(t, outdir):
    p = OnePager(t["title"], t["subtitle"], (30, 130, 120))
    p.header()
    p.field_row(t["field"], lines=1)
    p.section(t["clothing"])
    p.checklist(t["clothing_items"], cols=2)
    p.section(t["toiletries"])
    p.checklist(t["toiletries_items"], cols=2)
    p.section(t["tech"])
    p.checklist(t["tech_items"], cols=2)
    p.section(t["last"])
    p.checklist(t["last_items"], cols=3)
    p.footer()
    p.output(str(outdir / "packing.pdf"))


def build_goal(t, outdir):
    p = OnePager(t["title"], t["subtitle"], (20, 130, 90))
    p.header()
    p.field_row(t["field"], lines=1)
    p.section(t["smart"])
    p.field_row(t["s"], lines=1)
    p.field_row(t["m"], lines=1)
    p.field_row(t["a"], lines=1)
    p.field_row(t["r"], lines=1)
    p.field_row(t["t"], lines=1)
    p.section(t["actions"])
    p.field_row(t["a1"], lines=1)
    p.field_row(t["a2"], lines=1)
    p.field_row(t["a3"], lines=1)
    p.section(t["milestones"])
    p.field_row(t["m1"], lines=1)
    p.footer()
    p.output(str(outdir / "goal.pdf"))


def build_workout(t, outdir):
    p = OnePager(t["title"], t["subtitle"], (30, 120, 110))
    p.header()
    p.field_row(t["field"], lines=1)
    p.section(t["workouts"])
    p.table(t["headers"], [[""] * len(t["headers"]) for _ in range(12)],
            [22, 56, 34, 28, 51.9])
    p.section(t["progress"])
    p.field_row(t["progress_body"], lines=1)
    p.footer()
    p.output(str(outdir / "workout.pdf"))


PRODUCTS = {
    "sales": build_sales,
    "budget": build_budget,
    "habit": build_habit,
    "meal": build_meal,
    "password": build_password,
    "packing": build_packing,
    "goal": build_goal,
    "workout": build_workout,
}


def main():
    OUT.mkdir(exist_ok=True)
    count = 0
    for lang, name in LANGS.items():
        outdir = OUT / lang
        outdir.mkdir(exist_ok=True)
        for prod, builder in PRODUCTS.items():
            builder(STRINGS[lang][prod], outdir)
            count += 1
        print(f"{lang:2s} ({name}): {len(PRODUCTS)} PDFs → {outdir.relative_to(BASE)}/")
    print(f"\nDone — {count} translated PDFs in {OUT.relative_to(BASE)}/")


if __name__ == "__main__":
    main()
