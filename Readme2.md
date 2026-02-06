# Serverless 배포/권한 에러 정리

> 공개용으로 민감정보(계정 ID, ARN, 사용자명 등)는 마스킹했습니다.

## 1) Serverless 개요 (Node.js)
Node.js 환경에서 말하는 **Serverless**는 서버가 없다는 뜻이 아니라,
**서버 인프라 관리를 직접 하지 않고 코드 실행만 집중**하는 개발 방식입니다.

| 기능 | 설명 |
| --- | --- |
| 서버 없이 코드 실행 | Express/Koa 없이 `handler.js` 함수만 실행 |
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

## 2) CloudFormation 권한 오류
에러 예시:
```
User: arn:aws:iam::<ACCOUNT_ID>:user/<IAM_USER> is not authorized to perform: cloudformation:CreateChangeSet ...
```
원인:
- IAM 사용자에 CloudFormation 권한이 없음

대응:
- AWS 콘솔 → IAM → 사용자 → 권한 탭 → 정책 추가

![CloudFormation 권한 추가](image-15.png)
![정책 확인](image-16.png)

## 3) API Gateway 권한 오류
에러 예시:
```
... not authorized to perform: apigateway:PUT on resource: arn:aws:apigateway:ap-northeast-2::/tags/arn%3Aaws%3Aapigateway%3Aap-northeast-2%3A%3A%2Frestapis%2F* ...
```
원인:
- API Gateway 관련 권한 부족

대응:
- API Gateway 관련 권한 추가

![API Gateway 권한](image-17.png)
![API Gateway 권한 상세](image-18.png)

## 4) CloudFormation 스택 롤백 오류
에러 예시:
```
Stack:arn:aws:cloudformation:ap-northeast-2:<ACCOUNT_ID>:stack/hello-api-dev/<STACK_ID> is in UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS state and can not be updated.
```
대응:
- 스택 삭제 후 재시도
  ```bash
  aws cloudformation delete-stack --stack-name hello-api-dev
  ```

![스택 에러](image-19.png)
![삭제 성공](image-20.png)
![삭제 실패 시 전체 삭제](image-21.png)

## 5) CloudWatch Logs 권한 오류
에러 예시:
```
User with accountId: <ACCOUNT_ID> is not authorized to perform CreateLogGroup with Tags. An additional permission "logs:TagResource" is required.
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

## 6) Log Group AlreadyExists 오류
에러 예시:
```
Resource of type 'AWS::Logs::LogGroup' with identifier '{"/properties/LogGroupName":"/aws/lambda/<FUNCTION_NAME>"}' already exists.
```
대응:
- 기존 Log Group 삭제 후 재실행

![Log Group 중복](image-32.png)
![완료 화면](image-33.png)
