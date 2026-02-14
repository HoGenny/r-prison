from pydantic import BaseModel, Field


class TokenPair(BaseModel):
    """자체 JWT 토큰 쌍 (access + refresh)."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class KakaoLoginRequest(BaseModel):
    """RN 앱에서 카카오 SDK로 발급받은 access_token을 전달."""
    kakao_access_token: str

class SetupNicknameRequest(BaseModel):
    """신규 유저 닉네임 설정 요청. 2~16자."""
    nickname: str = Field(min_length=2, max_length=16)

class RefreshRequest(BaseModel):
    """토큰 갱신 / 로그아웃 요청. refresh_token을 body에 전달."""
    refresh_token: str
class KakaoLoginResponse(BaseModel):
    """
    카카오 로그인 응답.
    - is_new=True: 신규 유저 → 프론트에서 닉네임 설정 화면으로 이동
    - is_new=False: 기존 유저 → 바로 홈 화면
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    is_new: bool