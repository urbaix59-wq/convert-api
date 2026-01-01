from pathlib import Path
import uuid

from fastapi import FastAPI, UploadFile, File, Request, Header, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from convert import convert_file

# ---------------------------------------------------------
# CLÉ D’API (TU PEUX LA CHANGER)
# ---------------------------------------------------------
API_KEY = "CLE_API_DE_YOUCEF_2024_SUPER_SECRETE"

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# PAGE WEB (interface utilisateur)
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------------------------------------------------
# API PUBLIQUE AVEC CLÉ D’API
# ---------------------------------------------------------
@app.post("/api/v1/convert")
async def api_convert(
    file: UploadFile = File(...),
    x_api_key: str = Header(None)
):
    # Vérification de la clé API
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Clé API invalide")

    # Sauvegarde du fichier uploadé
    original_name = Path(file.filename)
    suffix = original_name.suffix.lower()
    temp_id = uuid.uuid4().hex

    input_path = UPLOAD_DIR / f"{temp_id}{suffix}"
    data = await file.read()
    input_path.write_bytes(data)

    # Conversion
    output_path = convert_file(input_path)

    if not Path(output_path).exists():
        return JSONResponse(
            {"success": False, "error": "La conversion a échoué."},
            status_code=500,
        )

    # Réponse JSON propre
    return {
        "success": True,
        "original_filename": original_name.name,
        "output_filename": Path(output_path).name,
        "download_url": f"/download/{Path(output_path).name}",
    }


# ---------------------------------------------------------
# TÉLÉCHARGEMENT DU FICHIER CONVERTI
# ---------------------------------------------------------
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        return JSONResponse({"error": "Fichier introuvable."}, status_code=404)

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename,
    )


# ---------------------------------------------------------
# ENDPOINT /convert (optionnel, pour ton interface web)
# ---------------------------------------------------------
@app.post("/convert")
async def convert_endpoint(file: UploadFile = File(...)):
    original_name = Path(file.filename)
    suffix = original_name.suffix.lower()
    temp_id = uuid.uuid4().hex

    input_path = UPLOAD_DIR / f"{temp_id}{suffix}"
    data = await file.read()
    input_path.write_bytes(data)

    output_path = convert_file(input_path)

    if not Path(output_path).exists():
        return JSONResponse(
            {"error": "La conversion a échoué."},
            status_code=500,
        )

    download_name = f"{original_name.stem}.pdf"

    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename=download_name,
    )
