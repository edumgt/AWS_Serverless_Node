# AWS Serverless Node 학습 정리 (공개용)

> 공개 공유를 위해 민감정보(계정 ID, ARN, 개인 링크, API ID 등)는 마스킹했습니다.

## 1) 참고 링크
- Fork 필요 GitHub
  - https://github.com/Carlosrincong/AWS-Solutions-Architect-Associate
  - https://github.com/stacksimplify/aws-eks-kubernetes-masterclass
  - https://github.com/stacksimplify/kubernetes-fundamentals
  - https://github.com/stacksimplify/docker-fundamentals
- Notion
  - CodePipeline: <REDACTED_NOTION_URL>
  - Role/Pipeline/EKS: <REDACTED_NOTION_URL>

## 2) AWS Well-Architected
- AWS 공식 아키텍처 사례: https://aws.amazon.com/ko/architecture

![Well-Architected 소개](image-37.png)
![Well-Architected 참고](image-38.png)

## 3) 구성도 작성
- ChatGPT에 구성도 이미지 업로드 후 분석
  - <REDACTED_CHATGPT_SHARE_URL>
- draw.io에서 구성도 작성 후 GitHub 연동 저장

![draw.io 구성도 작성](image-39.png)
![GitHub 연동/저장](image-40.png)

## 4) Serverless 개요 (Node.js)
Node.js에서 말하는 “Serverless”는 **서버가 없다는 의미가 아니라**,
**서버 인프라 관리 없이 코드 실행에 집중**하는 방식입니다.

| 기능 | 설명 |
| --- | --- |
| 서버 없이 코드 실행 | Express/Koa 서버 없이 `handler.js` 함수만 실행 |
| 요청마다 자동 인스턴스 | 요청 시 Lambda 자동 실행 |
| 사용량 기반 과금 | 초 단위 과금, 항상 켜둘 필요 없음 |
| 인프라 자동 구성 | Serverless Framework으로 API Gateway, IAM, Lambda 자동 설정 |
| 배포 자동화 | `serverless deploy`로 배포 (API URL 포함) |

| 항목 | 전통적인 Node.js 서버 (Express 등) | Serverless (Lambda + API Gateway) |
| --- | --- | --- |
| 서버 유지 | EC2, PM2 등 상시 실행 | 요청 시 자동 실행 |
| 비용 | 항상 켜두므로 요금 발생 | 호출 시만 과금 |
| 배포 | 수동 (ssh, git pull, 재시작 등) | 자동 배포 (`serverless deploy`) |
| 관리 | 인스턴스/로드밸런서/보안 직접 관리 | AWS가 관리 (IAM, 보안, 스케일 등 포함) |
| 성능 튜닝 | 직접 조절 필요 | 동시성 자동 관리, 콜드스타트 주의 |

## 5) API Gateway 개요
API Gateway는 클라이언트(웹/앱 등)와 백엔드(Lambda, EC2 등) 사이의 **중간 관문** 역할을 합니다.

![API Gateway 설정 화면](image.png)

| 역할 | 설명 |
| --- | --- |
| 요청 라우팅 | URL 경로/HTTP 메서드 기준으로 Lambda, EC2 등 분기 |
| 보안 처리 | 인증/인가 (IAM, Cognito, API Key, JWT 등) |
| 속도 제한 | 초당 요청 수 제한 (Throttle) |
| 로깅/모니터링 | CloudWatch Logs 연동 |
| CORS 관리 | 브라우저 API 호출 허용 설정 |
| 응답 변환 | JSON/XML 포맷 변경/필터링 |
| 서버리스 연결 | Lambda와 바로 연결 가능 |

## 6) Lambda 함수 생성
- `index.js` 작성 후 압축
  - `Compress-Archive -Path index.js -DestinationPath function.zip`
  - 일반 압축 툴 사용 가능
- Lambda 함수 생성 명령
  ```bash
  aws lambda create-function \
    --function-name edumgt-lambda-api \
    --runtime nodejs20.x \
    --role arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME> \
    --handler index.handler \
    --zip-file fileb://function.zip \
    --region ap-northeast-2
  ```

![Lambda 함수 생성 결과](image-1.png)

## 7) API Gateway REST API 생성 및 Lambda 연동
1. REST API 생성 (AWS Console > API Gateway > REST API)
2. Lambda 함수 연결: `edumgt-lambda-api`

![Lambda 함수 연결](image-2.png)
![Lambda 함수 연결 상세](image-3.png)

3. 새 리소스 `/hello` 추가

![리소스 생성](image-5.png)
![리소스 확인](image-4.png)

4. 우측 메서드 생성 클릭

![메서드 생성 버튼](image-6.png)
![메서드 생성 선택](image-7.png)
![메서드 생성 입력](image-8.png)

5. 메서드 생성 확인 및 배포

![메서드 생성 확인](image-9.png)

6. GET 메서드 추가 → Lambda 통합 설정

![GET 메서드 Lambda 통합](image-10.png)

7. URL 확인 (목록 중 ID 포함)
- 예: `https://<API_ID>.execute-api.ap-northeast-2.amazonaws.com/dev`

![배포 URL 확인](image-11.png)

8. 스테이지 생성 후 재배포

![스테이지 생성](image-12.png)
![재배포](image-13.png)

9. 기존 API 리소스 삭제 후 재생성 (재배포 시 주의)

![리소스 재생성](image-14.png)

## 8) Serverless Framework 배포 오류 및 권한 정리
### 8-1. CloudFormation 권한 오류
에러:
```
User ... is not authorized to perform: cloudformation:CreateChangeSet ...
```
대응:
- IAM 사용자에 CloudFormation 권한 부여
- AWS Console → IAM → 사용자 → 권한 탭 → 정책 추가

![CloudFormation 권한 추가](image-15.png)
![정책 확인](image-16.png)

### 8-2. API Gateway 권한 오류
에러:
```
... not authorized to perform: apigateway:PUT ...
```
대응:
- API Gateway 관련 권한 추가

![API Gateway 권한](image-17.png)
![API Gateway 권한 상세](image-18.png)

### 8-3. CloudFormation 스택 롤백 오류
에러:
```
... UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS ...
```
대응:
- 스택 삭제 후 재시도
  ```bash
  aws cloudformation delete-stack --stack-name hello-api-dev
  ```
- 삭제 성공 시 화면

![스택 에러](image-19.png)
![삭제 성공](image-20.png)
![삭제 실패 시 전체 삭제](image-21.png)

### 8-4. CloudWatch Logs 권한 오류
에러:
```
... not authorized to perform CreateLogGroup with Tags ...
```
대응:
- `logs:TagResource` 권한 추가 필요

![CloudWatch Logs 권한 오류](image-22.png)
![권한 추가](image-23.png)
![권한 추가 상세](image-24.png)

에러 반복 시 정책 직접 생성

![정책 생성](image-25.png)
![정책 생성 상세](image-26.png)
![정책 생성 옵션](image-27.png)
![정책 생성 옵션 2](image-28.png)
![정책 생성 완료](image-29.png)

추가 설정

![추가 설정 1](image-30.png)
![추가 설정 2](image-31.png)

### 8-5. Log Group AlreadyExists 오류
에러:
```
Resource of type 'AWS::Logs::LogGroup' ... already exists.
```
대응:
- 기존 Log Group 삭제 후 재실행

![Log Group 중복](image-32.png)
![완료 화면](image-33.png)

## 9) AWS CLI 연습
- S3 버킷 생성
  ```bash
  aws s3 mb s3://<BUCKET_NAME>
  ```

![S3 버킷 생성](image-36.png)

- S3 목록 확인
  ```bash
  aws s3 ls
  aws s3 ls s3://<BUCKET_NAME>/
  ```

- 로그 확인
  ```bash
  aws logs describe-log-groups
  aws logs describe-log-streams --log-group-name <LOG_GROUP_NAME>
  aws logs get-log-events --log-group-name <LOG_GROUP_NAME> --log-stream-name <LOG_STREAM_NAME>
  ```

![CloudWatch Logs 조회](image-35.png)

## 10) 추가 참고 이미지

![추가 참고 이미지](https://github.com/user-attachments/assets/6f7ae91d-6d57-4221-bc52-b11bdfc81df0)
