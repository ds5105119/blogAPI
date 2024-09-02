## 프로젝트 개요

DRF로 만든 블로그의 API 서버입니다. 다양한 장고의 third-party 앱을 사용하였습니다

## WBS

![Frame 48](https://github.com/user-attachments/assets/925f4acd-8198-45ae-a4ac-61a47b10596b)

## ERD

<img width="1422" alt="스크린샷 2024-09-02 오전 8 41 12" src="https://github.com/user-attachments/assets/b9c94bbe-abcb-47a5-85e1-6a69bbbb0f52">

## 사용 기술 및 선택 이유

### Django

- Django-Rest-Framework
    - DRF는 강력한 시리얼라이저와 뷰셋을 제공하여 API 개발 과정을 간소화합니다. 또한, 다양한 인증 방식과 권한 관리 기능을 지원하여 보안성 높은 API를 구현할 수 있습니다. 이를 통해 클라이언트와 서버 간의 효율적인 데이터 교환이 가능해집니다.
    - Django Rest Framework를 활용하여 RESTful API 서버를 구축하는 것이 목표입니다.
- Django Allauth
    - Django Allauth는 다양한 소셜 인증 제공업체를 지원하며, 유연한 인증 시스템을 구현할 수 있게 해줍니다. 이를 통해 사용자는 편리하게 소셜 계정으로 로그인할 수 있으며, 개발자는 복잡한 인증 로직을 간소화할 수 있습니다. Adapter를 통한 커스터마이징이 용이합니다.
    - 최신 Allauth를 사용합니다.
- DJ-Rest-Auth
    - DJ-Rest-Auth는 Django Rest Framework와 Django Allauth를 통합하여 RESTful API에 대한 인증 기능을 제공합니다.
    - 최신 Allauth와 호환성 문제가 있어, 최신 Allauth와 호환되도록, `*dj_rest_auth.registration.serializers.SocialLoginSerializer`를 상속받아 `validate` 함수를 수정하였습니다.* 수정된 코드는 DJ-Rest-Auth가 업데이트 되어도 Robust함을 보장합니다. (accounts/serializers.py)
- DjangoRestFramework-SimpleJWT
    - DjangoRestFramework-SimpleJWT는 (JWT) 인증을 Django REST Framework에 통합하는 라이브러리입니다. 이는 안전하고 stateless한 인증 메커니즘을 제공하여, 서버의 부하를 줄이고 확장성을 향상시킵니다.
    - JWT 토큰의 상세 Config는 [Settings.py](http://Settings.py) 참조
- Django-Taggit
    - Tag 기능

### NEXT.js

- 프론트 엔드를 구현하기 위해 사용하였습니다.
- Axios
    - Axios Instance를 사용한 API 패키징
    - Axios interceptors를 사용한 API 패키징
- React-Query
    - 전역 상태 관리를 위해 사용
- MDX Editor
    - /src/components/editor/ 내 파일들
    - MDX WYSIWYG 에디터를 구현하기 위해 사용하였습니다.
    - Code Editor, MD 형식 Keyboard Shortcut(```, `, # 등)을 지원합니다.
    - 커스텀 이미지 최적화 기능을 통해 S3버킷으로 업로드됩니다.

## 기능

**1. 사용자 인증 및 프로필** 

- 커스텀 유저
    - AbstractBaseUser 상속을 통한 커스텀 유저 기능 구현
- 프로필 상세 보기 기능
- Allauth, Dj-rest-auth, simpleJWT를 통한 JWT기반 소셜 로그인 구현

**2. 게시물 관리**

- 게시물 CRUD
- 게시물 LIST

**3. 댓글 시스템** 

- 댓글 작성, 수정, 삭제

**4. 카테고리 및 태그**

- 태그 목록 및 태그별 게시물 보기
- 태그 상세 정보 페이지

## 후기
두 프레임워크를 동시에 짧은 시간동안 소화해내며 백개가까이 되는 라이브러리를 사용하다 보니 꽤나 공을 들인 프로젝트였습니다.
백엔드 개발자를 희망하고 있지만 백엔드와 프론트 사이에서의 데이터 교환에 대한 심도 높은 이해를 위해서는 어느정도 프론트에서 직접 구현해보는 것 또한 좋은 경험이 될 것이라 생각을 하고 풀스택 개발을 하였습니다.
본 프로젝트를 통해 프론트와 백엔드 사이에서의 데이터 교환 방법, 페이지네이션, CORS와 같은 보안 설정들까지 매우 심도 깊게 DRF와 NEXT JS를 사용해본 것 같습니다.
