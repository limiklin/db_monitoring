# db_monitoring

DB Event Monitoring System (Dooray Webhook Alert)

MariaDB의 db_event_log / db_event 데이터를 기반으로
배치 작업 지연·미완료 이벤트를 자동 감지하고 Dooray Webhook으로 알림을 전송하는 모니터링 시스템입니다.

Windows 환경에서는 daemon을 사용할 수 없기 때문에
Windows Task Scheduler(작업 스케줄러)가 1분 또는 5분 주기로 Python 스크립트를 실행하여
에러 감지 및 알림을 수행합니다.

또한, 같은 에러에 대해 하루 1번만 알림을 보냄으로써
중복 알림을 방지하는 구조로 설계되었습니다.
