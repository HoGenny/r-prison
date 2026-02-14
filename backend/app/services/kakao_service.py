from __future__ import annotations

import httpx

from app.core.errors import AppError


# 카카오 사용자 정보 조회 API 엔드포인트
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


class KakaoService:
    async def get_kakao_user(self, kakao_access_token: str) -> dict:
        """
        카카오 access_token으로 사용자 정보를 조회한다.

        Args:
            kakao_access_token: RN 카카오 SDK에서 발급받은 access_token

        Returns:
            {"kakao_id": 12345678} — 카카오 고유 회원번호 (Signed int 64)

        Raises:
            AppError(401): 토큰이 유효하지 않거나 카카오 API 호출 실패
        """
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                KAKAO_USER_ME_URL,
                headers={
                    "Authorization": f"Bearer {kakao_access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )

        if resp.status_code != 200:
            raise AppError(
                "Failed to verify Kakao token",
                status_code=401,
                code="kakao_auth_failed",
            )

        data = resp.json()
        kakao_id = data.get("id")
        if kakao_id is None:
            raise AppError(
                "Invalid Kakao response",
                status_code=401,
                code="kakao_auth_failed",
            )

        return {"kakao_id": kakao_id}


kakao_service = KakaoService()
