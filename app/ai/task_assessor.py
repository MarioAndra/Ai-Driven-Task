# app/ai/task_assessor.py

import copy
import json
import random
from pathlib import Path

from .constants import (
    CANDIDATE_LABELS, LABEL_TO_TOPIC, QUESTION_TEMPLATES,
    DEFAULT_WEIGHTS, GA_CONFIG
)
from .utils import (
    similarity, get_task_keywords_from_task_text, tournament_select,
    crossover_weights, mutate_weights
)

USE_HF = False
try:
    from transformers import pipeline
except ImportError:
    USE_HF = False

HF_MODEL = "joeddav/xlm-roberta-large-xnli"
CONF_THRESH = 0.50
MAX_QUESTIONS = 25

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "data" / "model_weights.json"


def simple_keyword_extract(description):
    desc = description.lower()
    detected = {}
    for label in CANDIDATE_LABELS:
        if label.lower() in desc:
            mapping = LABEL_TO_TOPIC.get(label)
            if mapping:
                topic, value = mapping
                detected.setdefault(topic, set()).add(value)
    return {k: list(v) for k, v in detected.items()}


def hf_zero_shot_extract(description):
    try:
        classifier = pipeline("zero-shot-classification", model=HF_MODEL)
    except Exception as e:
        print(f"HF pipeline unavailable: {e}")
        return None

    result = classifier(description, candidate_labels=CANDIDATE_LABELS, multi_label=True)
    detected = {}
    labels = result.get("labels", [])
    scores = result.get("scores", [])

    for lbl, score in zip(labels, scores):
        if score >= CONF_THRESH:
            mapping = LABEL_TO_TOPIC.get(lbl)
            if mapping:
                topic, value = mapping
                detected.setdefault(topic, set()).add(value)
            else:
                detected.setdefault("misc", set()).add(lbl)
    return {k: list(v) for k, v in detected.items()}


def extract_details_from_description(description):
    if USE_HF:
        detected = hf_zero_shot_extract(description)
        if detected is not None:
            return detected

    return simple_keyword_extract(description)


def topic_matches_prefilled(topic, prefilled):
    if not prefilled:
        return False

    mapping_keys = {
        "framework": ["framework_backend", "framework_frontend"],
        "database": ["database"],
        "infrastructure": ["infrastructure", "hosting"],
        "payments": ["payments"],
        "design": ["design_responsive", "logo"],
        "apis": ["apis", "realtime"],
        "testing": ["testing"],
        "auth": ["auth"],
        "devops": ["devops", "infrastructure"],
    }
    keys_to_check = mapping_keys.get(topic, [topic])

    for key in keys_to_check:
        if key in prefilled and prefilled[key]:
            return True
    return False


def generate_questions(project_description, prefilled_details):
    questions = []
    for topic, template_questions in QUESTION_TEMPLATES.items():
        if not topic_matches_prefilled(topic, prefilled_details):
            questions.extend(template_questions)

    unique_questions = list(dict.fromkeys(questions))
    return unique_questions[:MAX_QUESTIONS]


def build_subtasks_from_answers(answers_dict, prefilled_details):
    subtasks = []
    if prefilled_details:
        if prefilled_details.get("framework_backend"):
            for v in prefilled_details["framework_backend"]:
                subtasks.append(f"Setup backend stack: {v} (create project skeleton and README)")
        if prefilled_details.get("framework_frontend"):
            for v in prefilled_details["framework_frontend"]:
                subtasks.append(f"Setup frontend stack: {v} (create project skeleton and README)")
        if prefilled_details.get("database"):
            for v in prefilled_details["database"]:
                subtasks.append(f"Design and provision database: {v} (schema, migrations, backups)")
        if prefilled_details.get("hosting"):
            for v in prefilled_details["hosting"]:
                subtasks.append(f"Prepare hosting on: {v} (staging + production)")
        if prefilled_details.get("payments"):
            for v in prefilled_details["payments"]:
                subtasks.append(f"Integrate payment gateway: {v}")
        if prefilled_details.get("storage"):
            for v in prefilled_details["storage"]:
                subtasks.append(f"Configure storage/CDN: {v} (images/media)")
        if prefilled_details.get("apis"):
            for v in prefilled_details["apis"]:
                subtasks.append(f"Design API: {v} endpoints and documentation")
        if prefilled_details.get("realtime"):
            for v in prefilled_details["realtime"]:
                subtasks.append(f"Implement realtime features using: {v}")
        if prefilled_details.get("frontend_lib"):
            for v in prefilled_details["frontend_lib"]:
                subtasks.append(f"Integrate frontend library: {v}")
        if prefilled_details.get("infrastructure"):
            for v in prefilled_details["infrastructure"]:
                subtasks.append(f"Plan infra using: {v} (Docker/K8s/Terraform as needed)")
        if prefilled_details.get("mobile"):
            for v in prefilled_details["mobile"]:
                subtasks.append(f"Plan mobile approach: {v}")
        if prefilled_details.get("accessibility"):
            for v in prefilled_details["accessibility"]:
                subtasks.append("Include accessibility (a11y) checks and WCAG guidance")
        if prefilled_details.get("security_compliance"):
            for v in prefilled_details["security_compliance"]:
                subtasks.append(f"Address compliance/security: {v}")

    q_auth_methods = "What user registration and authentication methods are required? (email/password, OAuth/social login like Google/Facebook, phone/SMS, SSO)."
    if q_auth_methods in answers_dict:
        auth_method = answers_dict[q_auth_methods].lower()
        if auth_method not in ['no', 'none', 'n']:
            if 'social' in auth_method or 'oauth' in auth_method:
                subtasks.append("Implement social/OAuth login (Google, Facebook, etc.)")
            if 'email' in auth_method or 'password' in auth_method:
                subtasks.append("Implement secure email/password registration and login")
            if 'sso' in auth_method:
                subtasks.append("Integrate SSO provider (SAML/OIDC)")

    q_password = "Should password recovery, email verification, or multi-factor authentication be implemented?"
    if q_password in answers_dict:
        pw_features = answers_dict[q_password].lower()
        if pw_features not in ['no', 'none', 'n']:
            if 'email verification' in pw_features:
                subtasks.append("Implement email verification feature")
            if 'password recovery' in pw_features:
                subtasks.append("Implement secure password recovery flow")
            if 'multi-factor' in pw_features or '2fa' in pw_features:
                subtasks.append("Add multi-factor authentication (TOTP / SMS)")

    q_db = "Which database type do you prefer? (SQL: Postgres/MySQL, NoSQL: MongoDB/DynamoDB)? Specify version if known."
    if q_db in answers_dict and answers_dict[q_db].strip():
        db_choice = answers_dict[q_db].strip()
        if db_choice not in ['no', 'none', 'n']:
            subtasks.append(f"Design DB schema & migration strategy for: {db_choice}")

    q_infra = "Where will the app be hosted? (AWS, Azure, GCP, DigitalOcean, or on-prem?)."
    if q_infra in answers_dict and answers_dict[q_infra].strip():
        infra = answers_dict[q_infra].strip()
        subtasks.append(f"Prepare hosting plan for: {infra}")

    q_infra2 = "Do you need Docker, Kubernetes, serverless, or VMs?"
    if q_infra2 in answers_dict and answers_dict[q_infra2].strip():
        cont = answers_dict[q_infra2].lower()
        if cont not in ['no', 'none', 'n']:
            if "docker" in cont:
                subtasks.append("Dockerize services with Dockerfiles")
            if "kubernetes" in cont:
                subtasks.append("Create K8s manifests/Helm charts")
            if "serverless" in cont:
                subtasks.append("Design serverless function layout and deployments")

    q_payments = "What payment gateways should be integrated? (Stripe, PayPal, local bank?)."
    if q_payments in answers_dict and answers_dict[q_payments].strip():
        subtasks.append(f"Integrate payment gateways: {answers_dict[q_payments].strip()}")

    q_payments2 = "Do you need recurring payments, refunds, or multi-currency?"
    if q_payments2 in answers_dict and answers_dict[q_payments2].strip():
        rec = answers_dict[q_payments2].lower()
        if rec not in ['no', 'none', 'n']:
            if 'recurring' in rec:
                subtasks.append("Enable recurring payments/subscriptions")
            if 'refund' in rec:
                subtasks.append("Implement refund mechanism and reconciliation")
            if 'multi-currency' in rec:
                subtasks.append("Support multi-currency pricing & payments")

    q_design_resp = "Should the site be mobile-first / responsive? Any target device priorities?"
    if q_design_resp in answers_dict and answers_dict[q_design_resp].strip():
        resp = answers_dict[q_design_resp].lower()
        if resp not in ['no', 'none', 'n']:
            if 'mobile' in resp:
                subtasks.append("Implement mobile-first responsive UI and test breakpoints")
            else:
                subtasks.append("Implement responsive UI for desktop/tablet/mobile")

    q_logo = "Do you need a logo / brand kit? Who supplies them?"
    if q_logo in answers_dict and answers_dict[q_logo].strip():
        logo_ans = answers_dict[q_logo].strip().lower()
        if any(x in logo_ans for x in ["yes", "y", "true", "create", "design", "need"]):
            subtasks.append("Create logo and basic brand kit (colors, typography)")
        if any(x in logo_ans for x in ["client", "provided", "existing", "have", "supplies", "supply"]):
            subtasks.append("Collect existing logo/brand assets and integrate into design system")

    q_api = "Will the project expose or require APIs (REST, GraphQL)? Do you need API docs (OpenAPI)?"
    if q_api in answers_dict and answers_dict[q_api].strip():
        api = answers_dict[q_api].lower()
        if api not in ['no', 'none', 'n']:
            if 'rest' in api or 'graphql' in api:
                subtasks.append("Design API endpoints and produce OpenAPI/GraphQL schema documentation")
            if 'webhook' in api:
                subtasks.append("Implement webhook endpoints with signature verification and retry logic")

    q_testing_strategy = "What testing strategies do you prefer? (unit, integration, e2e, load)."
    if q_testing_strategy in answers_dict and answers_dict[q_testing_strategy].strip():
        testing = answers_dict[q_testing_strategy].lower()
        if testing not in ['no', 'none', 'n']:
            if 'unit' in testing:
                subtasks.append("Write unit tests and setup coverage reporting")
            if 'integration' in testing:
                subtasks.append("Write integration tests for critical flows")
            if 'e2e' in testing or 'end-to-end' in testing:
                subtasks.append("Automate E2E user-journey tests (Cypress/Playwright)")
            if 'load' in testing or 'performance' in testing:
                subtasks.append("Create load/performance tests and benchmark targets")

    q_realtime = "Do you need real-time features? (WebSocket, push updates, live notifications)?"
    if q_realtime in answers_dict and answers_dict[q_realtime].strip():
        realtime_ans = answers_dict[q_realtime].lower()
        if realtime_ans not in ['no', 'none', 'n']:
            if 'websocket' in realtime_ans:
                subtasks.append("Implement real-time communication with WebSockets")
            if 'push' in realtime_ans:
                subtasks.append("Implement push updates for live data")
            if 'live notifications' in realtime_ans or 'notifications' in realtime_ans:
                subtasks.append("Implement live notification system for users")

    q_notifications = "Should the system send notifications? (Email, SMS, push notifications)?"
    if q_notifications in answers_dict and answers_dict[q_notifications].strip():
        notif_ans = answers_dict[q_notifications].lower()
        if notif_ans not in ['no', 'none', 'n']:
            if 'email' in notif_ans:
                subtasks.append("Setup email notification system (SMTP or service)")
            if 'sms' in notif_ans:
                subtasks.append("Setup SMS notification integration")
            if 'push' in notif_ans:
                subtasks.append("Setup push notification service for devices")

    q_inapp_notifications = "Do you need in-app notifications or alerts?"
    if q_inapp_notifications in answers_dict and answers_dict[q_inapp_notifications].strip():
        inapp_ans = answers_dict[q_inapp_notifications].lower()
        if inapp_ans not in ['no', 'none', 'n']:
            if 'yes' in inapp_ans or 'in-app' in inapp_ans or 'alerts' in inapp_ans:
                subtasks.append("Implement in-app notification/alert system")

    seen = set()
    dedup = []
    for s in subtasks:
        if s not in seen:
            dedup.append(s)
            seen.add(s)
    return dedup


def load_model_weights():
    if MODEL_PATH.exists():
        try:
            return json.loads(MODEL_PATH.read_text())
        except json.JSONDecodeError:
            print("Error loading model weights, using defaults.")
    return DEFAULT_WEIGHTS.copy()


def save_model_weights(weights):
    MODEL_PATH.write_text(json.dumps(weights, indent=2))


def find_relevant_employees_with_features(task_text, employees, similarity_threshold=0.25):
    task_keywords = get_task_keywords_from_task_text(task_text)
    candidates = []
    for emp in employees:
        if emp.get("status", "available") != "available":
            continue

        emp_skill_names = [s.get("name", "").lower() for s in emp.get("skills", [])]
        skill_levels = [float(s.get("rating", 3.0)) for s in emp.get("skills", [])]
        avg_skill_level = (sum(skill_levels) / len(skill_levels)) if skill_levels else 3.0

        total_match = sum(
            max(similarity(kw, sk) for sk in emp_skill_names) if emp_skill_names else 0 for kw in task_keywords)
        match_score = total_match / max(1, len(task_keywords))

        cap = emp.get("task_capacity")
        availability = max(0.0, 1.0 - (len(emp.get("assigned_tasks", [])) / cap)) if cap else 1.0

        if match_score >= similarity_threshold or avg_skill_level >= 3.0:
            candidates.append({
                "employee": emp,
                "match_score": match_score,
                "avg_skill_level": avg_skill_level,
                "availability": availability
            })
    return candidates


def compute_score_from_features(features, weights, task_difficulty=1.0):
    match_norm = max(0.0, min(1.0, features["match_score"]))
    exp_norm = max(0.0, min(1.0, (features["avg_skill_level"] - 1.0) / 4.0))
    avail_norm = max(0.0, min(1.0, features["availability"]))
    load_penalty = weights.get("w_load_penalty", 0.5) * features.get("current_load", 0)

    raw_score = (
            (weights.get("w_match", 1.0) * match_norm) +
            (weights.get("w_experience", 1.0) * exp_norm) +
            (weights.get("w_availability", 1.0) * avail_norm) -
            load_penalty
    )
    return raw_score / max(1.0, float(task_difficulty))


def assign_tasks_with_learning(subtasks: list[str], employees: list[dict], model_weights: dict = None):
    employees_copy = copy.deepcopy(employees)
    active_weights = model_weights or load_model_weights()
    print(f"\nUsing model weights: {active_weights}\n")

    assignments = []
    for task_text in subtasks:
        candidates = find_relevant_employees_with_features(task_text, employees_copy)

        scored_candidates = []
        for cand in candidates:
            if len(cand["employee"].get("assigned_tasks", [])) >= cand["employee"].get("task_capacity", 999):
                continue

            features = {
                "match_score": cand["match_score"],
                "avg_skill_level": cand["avg_skill_level"],
                "availability": cand["availability"],
                "current_load": len(cand["employee"].get("assigned_tasks", []))
            }
            score = compute_score_from_features(features, active_weights)
            scored_candidates.append({"employee": cand["employee"], "score": score, "features": features})

        if not scored_candidates:
            print(f"No available employees for: {task_text}")
            assignments.append({"task": task_text, "employee_name": None, "features": None})
            continue

        best_candidate = max(scored_candidates, key=lambda x: x["score"])
        chosen_emp = best_candidate["employee"]

        chosen_emp.setdefault("assigned_tasks", []).append(task_text)
        assignments.append({
            "task": task_text,
            "employee_name": chosen_emp.get("name"),
            "features": best_candidate["features"]
        })
        print(f"Assigned: {task_text} -> {chosen_emp.get('name')} (score {best_candidate['score']:.3f})")

    return assignments, employees_copy


def ga_optimize_weights(history, initial_weights=None):
    if not history:
        return initial_weights or DEFAULT_WEIGHTS.copy()

    data = [{
        "features": rec["features"],
        "feedback_norm": max(0.0, min(1.0, (float(rec["feedback"]) - 1.0) / 4.0))
    } for rec in history]

    def fitness_for_weights(w):
        weights = {
            "w_match": max(0.001, w[0]), "w_experience": max(0.001, w[1]),
            "w_availability": max(0.001, w[2]), "w_load_penalty": max(0.001, w[3])
        }
        mse = 0.0
        for d in data:
            pred = compute_score_from_features(d["features"], weights)
            total_weight = weights["w_match"] + weights["w_experience"] + weights["w_availability"]
            pred_norm = max(0.0, min(1.0, pred / total_weight if total_weight > 0 else 0))
            mse += (pred_norm - d["feedback_norm"]) ** 2
        return 1.0 / ((mse / len(data)) + 1e-9)

    init_w = initial_weights or DEFAULT_WEIGHTS
    pop = []
    for _ in range(GA_CONFIG["population_size"]):
        pop.append(tuple(max(0.001, random.gauss(init_w[k], 0.5)) for k in
                         ["w_match", "w_experience", "w_availability", "w_load_penalty"]))

    for _ in range(GA_CONFIG["generations"]):
        scored = sorted([(c, fitness_for_weights(c)) for c in pop], key=lambda x: x[1], reverse=True)

        elite_count = max(1, int(GA_CONFIG["elite_frac"] * GA_CONFIG["population_size"]))
        new_pop = [c for c, s in scored[:elite_count]]

        while len(new_pop) < GA_CONFIG["population_size"]:
            p1 = tournament_select(scored)
            p2 = tournament_select(scored)
            child = crossover_weights(p1, p2)
            child = mutate_weights(child, GA_CONFIG["mutation_rate"])
            new_pop.append(child)
        pop = new_pop

    best_w_tuple = max([(c, fitness_for_weights(c)) for c in pop], key=lambda x: x[1])[0]
    return {
        "w_match": best_w_tuple[0], "w_experience": best_w_tuple[1],
        "w_availability": best_w_tuple[2], "w_load_penalty": best_w_tuple[3]
    }


def evolve_model_from_db_history(db_history: list, initial_weights: dict):
    if not db_history:
        print("No history with feedback found. No model update.")
        return initial_weights

    best_weights = ga_optimize_weights(
        history=db_history,
        initial_weights=initial_weights
    )

    print(f"Updated model weights: {best_weights}")
    save_model_weights(best_weights)
    return best_weights