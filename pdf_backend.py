from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fpdf import FPDF
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/create-pdf")
async def create_pdf(
    title: str = "My PDF",
    files: list[UploadFile] = []
):
    try:
        print(f"Creating PDF with title: {title}")
        print(f"Number of files: {len(files)}")
        
        
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=False)
       
        for i, file in enumerate(files):
            print(f"Processing file {i+1}: {file.filename}")
            content = await file.read()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            
            pdf.add_page()
            
          
            pdf.image(tmp_path, x=20, y=20, w=257, h=170)
            
            
            os.unlink(tmp_path)

        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_pdf.close()
        
        pdf.output(temp_pdf.name)
        
       
        with open(temp_pdf.name, 'rb') as f:
            pdf_bytes = f.read()
        
        
        os.unlink(temp_pdf.name)
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={title.replace(' ', '_')}.pdf"}
        )
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return Response(content=str(e).encode(), status_code=500)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Image to PDF Converter API is starting...")
    print("📍 Server running at: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)