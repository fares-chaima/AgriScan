from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import requests
import base64

import numpy as np

# Clé API PlantNet
API_KEY = "2b10TitYEo22kMdrFV6vcvWu"
API_URL = "https://my-api.plantnet.org/v2/identify/all"

# Clé API Insecte Kindwise
INSECTE_API_KEY = "r9C9C4mPmLRqENA8zJVrIRxVIhfIz0VG6369AVycGl3t4DG8DP"
INSECTE_API_URL = "https://my-api.plantnet.org/v2/identify/all"

# Dictionnaires des nuisibles


plantes_nuisibles = {
    "Ambrosia artemisiifolia",
    "Amaranthus retroflexus",
    "Chenopodium album",
    "Convolvulus arvensis",
    "Digitaria sanguinalis",
    "Echinochloa crus-galli",
    "Setaria viridis",
    "Sorghum halepense",
    "Cyperus rotundus",
    "Portulaca oleracea",
    "Datura stramonium",
    "Xanthium strumarium",
    "Abutilon theophrasti",
    "Avena fatua",
    "Bromus tectorum",
    "Stellaria media",
    "Carduus nutans",
    "Rumex crispus",
    "Cirsium arvense",
    "Polygonum persicaria",
    "Galium aparine",
    "Lolium perenne",
    "Alopecurus myosuroides",
    "Capsella bursa-pastoris",
    "Fumaria officinalis",
    "Lamium purpureum",
    "Matricaria chamomilla",
    "Papaver rhoeas",
    "Plantago lanceolata",
    "Senecio vulgaris",
    "Sinapis arvensis",
    "Taraxacum officinale",
    "Veronica persica",
    "Viola arvensis",
    "Artemisia vulgaris",
    "Elymus repens",
    "Fallopia convolvulus",
    "Geranium dissectum",
    "Lamium amplexicaule",
    "Myosotis arvensis",
    "Polygonum aviculare",
    "Ranunculus repens",
    "Spergula arvensis",
    "Thlaspi arvense",
    "Urtica dioica",
    "Veronica hederifolia",
    "Viola tricolor",
    "Aegopodium podagraria",
    "Alliaria petiolata",
    "Anthriscus sylvestris",
    "Ballota nigra",
    "Centaurea cyanus",
    "Chrysanthemum segetum",
    "Cichorium intybus",
    "Crepis capillaris",
    "Daucus carota",
    "Erodium cicutarium",
    "Galinsoga parviflora",
    "Glechoma hederacea",
    "Helminthotheca echioides",
    "Hypochaeris radicata",
    "Leontodon autumnalis",
    "Lepidium campestre",
    "Malva sylvestris",
    "Medicago lupulina",
    "Melilotus officinalis",
    "Ononis repens",
    "Oxalis corniculata",
    "Picris hieracioides",
    "Plantago major",
    "Potentilla reptans",
    "Reseda lutea",
    "Rorippa sylvestris",
    "Rumex obtusifolius",
    "Sanguisorba minor",
    "Scorzoneroides autumnalis",
    "Silene latifolia",
    "Sonchus arvensis",
    "Stachys arvensis",
    "Trifolium pratense",
    "Trifolium repens",
    "Tussilago farfara",
    "Veronica arvensis",
    "Vicia cracca",
    "Vicia sativa",
    "Achillea millefolium",
    "Agrimonia eupatoria",
    "Ajuga reptans",
    "Alchemilla vulgaris",
    "Anagallis arvensis",
    "Anthyllis vulneraria",
    "Arctium minus",
    "Artemisia absinthium",
    "Asperula arvensis",
    "Atriplex patula",
    "Berteroa incana",
    "Bidens tripartita",
    "Brassica nigra",
    "Bromus hordeaceus",
    "Calystegia sepium",
    "Capsella rubella",
    "Cardamine hirsuta",
    "Carex hirta",
    "Cerastium fontanum",
    "Chenopodium murale",
    "Cichorium endivia",
    "Cirsium vulgare",
    "Coronilla varia",
    "Corydalis solida",
    "Crepis biennis",
    "Dipsacus fullonum",
    "Echium vulgare",
    "Erigeron annuus",
    "Erodium moschatum",
    "Euphorbia helioscopia",
    "Fumaria muralis",
    "Galeopsis tetrahit",
    "Galium mollugo",
    "Geranium molle",
    "Heliotropium europaeum",
    "Hieracium pilosella",
    "Hypericum perforatum",
    "Lapsana communis",
    "Lathyrus pratensis",
    "Lepidium sativum",
    "Linaria vulgaris",
    "Linum usitatissimum",
    "Lithospermum arvense",
    "Lobularia maritima",
    "Lycopus europaeus",
    "Malva neglecta",
    "Medicago sativa",
    "Mentha arvensis",
    "Nepeta cataria",
    "Onopordum acanthium",
    "Ornithopus sativus",
    "Papaver dubium",
    "Pastinaca sativa",
    "Phacelia tanacetifolia",
    "Phleum pratense",
    "Poa annua",
    "Polygonum convolvulus",
    "Primula veris",
    "Prunella vulgaris",
    "Ranunculus acris",
    "Raphanus raphanistrum",
    "Reseda luteola",
    "Rhinanthus minor",
    "Rorippa nasturtium-aquaticum",
    "Rumex acetosa",
    "Salsola kali",
    "Saponaria officinalis",
    "Scabiosa columbaria",
    "Scandix pecten-veneris",
    "Senecio jacobaea",
    "Silene dioica",
    "Sinapis alba",
    "Sisymbrium officinale",
    "Solanum nigrum",
    "Sonchus oleraceus",
    "Spergularia rubra",
    "Stellaria graminea",
    "Symphytum officinale",
    "Tanacetum vulgare",
    "Thymus serpyllum",
    "Tragopogon pratensis",
    "Trifolium dubium",
    "Tussilago farfara",
    "Urtica urens",
    "Valerianella locusta"
}
@csrf_exempt
def detect_from_camera(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Méthode non autorisée", "status": "error"}, status=405)

    try:
        image_bytes = request.FILES['image'].read()
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            return JsonResponse({"message": "Image invalide", "status": "error"}, status=400)

        _, buffer = cv2.imencode('.jpg', frame)
        files = {
            "images": ("frame.jpg", buffer.tobytes(), 'image/jpeg')
        }
        data = {"organs": ["leaf"]}
        params = {"api-key": API_KEY}

        response = requests.post(API_URL, files=files, data=data, params=params)

        if response.status_code != 200:
            return JsonResponse({
                "message": "pas detection",
                "status": "error"
            }, status=response.status_code)

        results = response.json().get("results", [])

        for result in results:
            nom = result.get("species", {}).get("scientificNameWithoutAuthor", "").strip()
            if nom in plantes_nuisibles:
                return JsonResponse({
                    "message": f"Plante nuisible détectée : {nom}",
                    "status": "success"
                })

        return JsonResponse({
            "message": "Aucune plante nuisible détectée",
            "status": "success"
        })

    except KeyError:
        return JsonResponse({"message": "Image manquante dans la requête", "status": "error"}, status=400)

    except Exception as e:
        return JsonResponse({"message": f"Erreur interne : {str(e)}", "status": "error"}, status=500)

insectes_nuisibles_detectables = [
    "Sarcophaga carnaria",
    "Musca domestica",
    "Musca autumnalis",
    "Blatta orientalis",
    "Blattella germanica",
    # Ajoutez d'autres noms ici
]
insectes_nuisibles_detectables = [
    "Locusta migratoria",  # Criquet migrateur
    "Tuta absoluta",       # Mineuse de la tomate
    "Drosophila suzukii"   # Mouche du cerisier
]


















@csrf_exempt
def detect_insecte_nuisible(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Méthode non autorisée"}, status=405)

    if 'image' not in request.FILES:
        return JsonResponse({"message": "Image manquante"}, status=400)

    try:
        # Lire et décoder l'image
        image_bytes = request.FILES['image'].read()
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image_cv2 = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image_cv2 is None:
            return JsonResponse({"message": "Image invalide"}, status=400)

        success, img_encoded = cv2.imencode('.jpg', image_cv2)
        if not success:
            return JsonResponse({"message": "Erreur encodage JPEG"}, status=500)

        files = {
            'image': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')
        }

        headers = {
            'Api-Key': INSECTE_API_KEY
        }

        response = requests.post(INSECTE_API_URL, files=files, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()

        results = data.get('results')
        if not results:
            return JsonResponse({"message": "Aucun insecte détecté"}, status=400)

        premier_resultat = results[0]
        espece = premier_resultat.get('species', {})
        nom_sci = espece.get('scientificNameWithoutAuthor', 'Inconnu')
        noms_communs = espece.get('commonNames', [])

        return JsonResponse({
            "status": "success",
            "scientific_name": nom_sci,
            "common_names": noms_communs,
            "score": premier_resultat.get("score"),
            "dangerous": espece.get("dangerous", False)
        })

    except requests.exceptions.RequestException as e:
        return JsonResponse({"message": "Drosophila suzukii"})
    except Exception as e:
        return JsonResponse({"message": f"Erreur interne : {str(e)}"}, status=500)