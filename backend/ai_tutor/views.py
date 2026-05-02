from utils.api import APIView, validate_serializer
from utils.decorators import login_required

from .serializers import AITutorRequestSerializer
from .services.providers import LLMProviderError
from .services.tutor import AITutorService


class AITutorAPI(APIView):
    @validate_serializer(AITutorRequestSerializer)
    @login_required
    def post(self, request):
        data = request.data
        try:
            result = AITutorService().generate(
                user=request.user,
                problem=data["problem"],
                code=data["code"],
                error_log=data.get("error_log", ""),
            )
        except ValueError as e:
            return self.error(str(e), err="rate-limit")
        except LLMProviderError as e:
            return self.error(str(e), err="ai-tutor-error")
        return self.success(result)

