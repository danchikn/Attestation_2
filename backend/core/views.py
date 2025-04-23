from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from .models import Resume
from .resume_parser_utils import extract_text_from_docx, extract_text_from_pdf, extract_skills


class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        resume = Resume.objects.create(user=request.user, file=file, parsed=True)
        return Response({
            "id": resume.id,
            "file": request.build_absolute_uri(resume.file.url),
            "uploaded_at": resume.uploaded_at,
            "parsed": resume.parsed
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, resume_id=None):
        if not resume_id:
            return Response({"error": "Resume ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            resume = Resume.objects.get(id=resume_id, user=request.user)
            resume.delete()
            return Response({"message": "Resume deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class ResumeAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resumes = Resume.objects.filter(user=request.user)
        data = []
        for resume in resumes:
            raw_text = ""
            skills = []
            if resume.file.name.endswith(".docx"):
                raw_text = extract_text_from_docx(resume.file.path)
            elif resume.file.name.endswith(".pdf"):
                raw_text = extract_text_from_pdf(resume.file.path)
            if raw_text:
                skills = extract_skills(raw_text)
            data.append({
                "id": resume.id,
                "filename": resume.file.name,
                "skills": skills,
                "raw_text": raw_text,
            })

        return Response(data)
