##
![image](https://github.com/user-attachments/assets/6f7ae91d-6d57-4221-bc52-b11bdfc81df0)

## https://www.notion.so/role-pipeline-EKS-pod-svc-fbe7709c01e74cd9819b2867decb6ab4

- role 목록

![Untitled (13).png](https://prod-files-secure.s3.us-west-2.amazonaws.com/ce3e1315-14c7-4e3e-ad28-d4aa4cd0f890/ee4b2fc8-306f-499a-b4d9-575c39b892f0/Untitled_(13).png)

- 위와 같이 4 종의 role 필요
- eksClusterRole, eksNodeRole 은 순수한 EKS 작업용

- codebuild.. 명칭의 role 은 codebuild repo 생성 시 AWS 추천 명칭으로 생성
- 해당 role 은 code build 및 ECR image push 역할
- 해당 role 연결정책
    - Container 사용 관련 정책 및 EKS, STS 신뢰 policy 필요
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/ce3e1315-14c7-4e3e-ad28-d4aa4cd0f890/bac94481-ffa8-4d76-9dec-546308cdb662/Untitled.png)
    

- 자동생성 정책

![Untitled (14).png](https://prod-files-secure.s3.us-west-2.amazonaws.com/ce3e1315-14c7-4e3e-ad28-d4aa4cd0f890/890bffdd-fa88-4708-aaaa-6d0c1736165e/Untitled_(14).png)

- 유관 작업을 위한 별도 생성 정책

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/ce3e1315-14c7-4e3e-ad28-d4aa4cd0f890/d418f157-defa-4d93-9c55-433706060e24/Untitled.png)

- kubectl 용 권한 - EksWorkshopKube.. 으로 명명

위와 동일한 정책 2가지 연결 필요

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/ce3e1315-14c7-4e3e-ad28-d4aa4cd0f890/64e3ffbb-7dd6-45ab-b059-202b12343c3d/Untitled.png)

- kubectl 의 role 위임을 위한 신뢰관계 - trust policy 필요

![Untitled (15).png](https://prod-files-secure.s3.us-west-2.amazonaws.com/ce3e1315-14c7-4e3e-ad28-d4aa4cd0f890/3d00ba5b-2377-4c9c-9d26-9d17d251365d/Untitled_(15).png)

- CodeBuild 의 주요 환경 변수

![Untitled (16).png](https://prod-files-secure.s3.us-west-2.amazonaws.com/ce3e1315-14c7-4e3e-ad28-d4aa4cd0f890/3618b870-01cd-443d-8cfe-3e53cad76ef2/Untitled_(16).png)

- user 예를들어 eksuser1 도 정책 할당

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/ce3e1315-14c7-4e3e-ad28-d4aa4cd0f890/48481ee5-6bb6-42db-b603-4d1ebfaf1a67/Untitled.png)

- EKS_KUBECTL_ROLE_ARN 변수 명에 role 기반 EksWorkshopKube.. 설정의 arn 매칭 필요
    - 해당 EKS_KUBECTL_ROLE_ARN 사용 buildspec.yml 내용
    
    ```jsx
    - CREDENTIALS=$(aws sts assume-role --role-arn $EKS_KUBECTL_ROLE_ARN --role-session-name Case-User --duration-seconds 900)
    - export AWS_ACCESS_KEY_ID="$(echo ${CREDENTIALS} | jq -r '.Credentials.AccessKeyId')"
    - export AWS_SECRET_ACCESS_KEY="$(echo ${CREDENTIALS} | jq -r '.Credentials.SecretAccessKey')"
    - export AWS_SESSION_TOKEN="$(echo ${CREDENTIALS} | jq -r '.Credentials.SessionToken')"
    - export AWS_EXPIRATION=$(echo ${CREDENTIALS} | jq -r '.Credentials.Expiration')
    - aws eks update-kubeconfig --name $EKS_CLUSTER_NAME
    ```
    
    - 해당 role 의 credential 정보 확인을 위해 Bastion Host 에서 해당 aws sts .. 구문 실행 필요
    
    ```jsx
    #vi .aws/credentials
    
    [default]
    aws_access_key_id = XXXXX
    aws_secret_access_key = XXXXX
    [eksuser]
    aws_access_key_id = XXXXX
    aws_secret_access_key = XXXXX
    
    ```
    
    ```jsx
    ubuntu@ip-172-31-38-166:~$ kubectl get svc
    NAME                  TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
    kubernetes            ClusterIP   10.100.0.1     <none>        443/TCP          6h37m
    springboot-crud-svc   NodePort    10.100.66.63   <none>        8080:30375/TCP   56m
    ubuntu@ip-172-31-38-166:~$ aws sts assume-role --role-arn arn:aws:iam::XXXXX:role/EksWorkshopCodeBuildKubectlRole --role-session-name test > assume-role-output.txt
    
    An error occurred (AccessDenied) when calling the AssumeRole operation: Roles may not be assumed by root accounts.
    ubuntu@ip-172-31-38-166:~$ vi .aws/credentials
    ubuntu@ip-172-31-38-166:~$ aws configure
    AWS Access Key ID [****************MOF5]: XXXXX
    AWS Secret Access Key [****************MkI+]: XXXXX
    Default region name [ap-northeast-2]: 
    Default output format [None]: 
    ubuntu@ip-172-31-38-166:~$ aws sts assume-role --role-arn arn:aws:iam::XXXXX:role/EksWorkshopCodeBuildKubectlRole --role-session-name test > assume-role-output.txt
    ubuntu@ip-172-31-38-166:~$ vi ./assume-role-output.txt
    ```
    
    ```jsx
    {
        "Credentials": {
            "AccessKeyId": "XXXXX",
            "SecretAccessKey": "XXXXX",
            "SessionToken": "XXXXX",
            "Expiration": "2024-05-05T07:37:15+00:00"
        },
        "AssumedRoleUser": {
            "AssumedRoleId": "XXXXX:test",
            "Arn": "arn:aws:sts::XXXXX:assumed-role/EksWorkshopCodeBuildKubectlRole/test"
        }
    }
    ```
    
    - 위의 json key - value 가 각각 변수로 치환되어 사용.
        
        ```jsx
        AWS_ACCESS_KEY_ID="$(echo ${CREDENTIALS} | jq -r '.Credentials.AccessKeyId')"
        AWS_SECRET_ACCESS_KEY="$(echo ${CREDENTIALS} | jq -r '.Credentials.SecretAccessKey')"
        AWS_SESSION_TOKEN="$(echo ${CREDENTIALS} | jq -r '.Credentials.SessionToken')"
        AWS_EXPIRATION=$(echo ${CREDENTIALS} | jq -r '.Credentials.Expiration')
        ```
