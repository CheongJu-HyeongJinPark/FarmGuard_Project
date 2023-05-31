from typing import Any

import requests
import xmltodict


def _get_pesticide(crop_name: str, disease: str, display_count: int = 10) -> Any:
    """
    농약안정정보시스템으로부터 농약등록정보를 가져옵니다

    Args:
        crop_name: 작물명
        disease: 병해충명
        display_count: 가져올 개수

    Returns:
        list[dict[str, Any]]
    """
    # 해충병에서 작물명을 제거합니다
    disease = disease.replace(crop_name, "")

    # 검색시 검색결과를 변질시키는 일부 값을 삭제합니다
    disease = disease.replace("반응", "").replace("시설", "")

    # 파프리카의 경우 작물명을 고추로 검색해야하기 때문에 예외처리
    if crop_name == "파프리카":
        crop_name = "고추"

    # 농약안전정보 OpenAPI 에 요청을 전송합니다
    response = requests.get(
        "http://psis.rda.go.kr/openApi/service.do",
        params={
            "apiKey": "20230517K7SKFZF1MHX486UGRTL1W",
            "serviceCode": "SVC01",
            "serviceType": "AA001",
            "cropName": crop_name,
            "diseaseWeedName": disease,
            "displayCount": display_count,
        },
        timeout=1000,
    )

    # XML 문서를 JSON 형태로 변환합니다
    return xmltodict.parse(response.content)


def get_pesticide(crop_name: str, disease: str) -> list[dict[str, Any]]:
    """
    농약안정정보시스템으로부터 농약등록정보를 가져옵니다

    Args:
        crop_name: 작물명
        disease: 병해충명

    Returns:
        list[dict[str, Any]]
    """
    # 검색 결과의 총 개수를 가져옵니다
    metadata = _get_pesticide(crop_name=crop_name, disease=disease)

    # 총 개수
    total_count = int(metadata["service"]["totalCount"])
    if total_count <= 0:
        return []

    data = _get_pesticide(crop_name=crop_name, disease=disease, display_count=total_count)
    try:
        # 응답 중 배열 형태의 자료를 추출합니다
        arr = data["service"]["list"]["item"]
        if isinstance(arr, list):
            return arr

        return []
    except (KeyError, TypeError):  # JSON 에 Key 가 존재하지 않거나, Null 값인 경우
        return []