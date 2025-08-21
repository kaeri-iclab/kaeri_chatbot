-- FAQ 테이블 생성
CREATE TABLE IF NOT EXISTS faq (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question VARCHAR NOT NULL,
    answer VARCHAR NOT NULL
);

-- Setting 테이블 생성
CREATE TABLE IF NOT EXISTS setting (
    id SERIAL PRIMARY KEY,
    key VARCHAR,
    query_model VARCHAR NOT NULL DEFAULT 'gpt-4o-mini',
    ai_model VARCHAR NOT NULL DEFAULT 'gpt-4o-mini'
);

-- FAQ 테이블이 비어있는지 확인하고 기본 데이터를 삽입
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM faq) THEN
        INSERT INTO faq (id, question, answer) VALUES
        (gen_random_uuid(), '한국원자력연구원은 어떤 기관인가요?', 
         '한국원자력연구원(KAERI)은 원자력의 연구개발을 종합적으로 수행하여 학술의 진보, 에너지 확보 및 원자력의 이용 촉진에 기여하는 것을 목적으로 하는 과학기술분야 정부출연연구기관입니다.'),
        (gen_random_uuid(), '한국원자력연구원은 언제 설립되었나요?', 
         '한국원자력연구원은 1959년 2월 3일에 원자력연구소라는 이름으로 설립되었습니다. 이는 한국 최초의 과학기술 연구기관으로, KIST보다 6년 앞서 설립되었습니다.'),
        (gen_random_uuid(), '한국원자력연구원의 주요 시설은 어디에 있나요?', 
         '한국원자력연구원의 본원은 대전광역시 유성구 대덕연구개발특구에 위치해 있습니다. 또한 정읍과 경주에 분원이 있습니다.'),
        (gen_random_uuid(), '한국원자력연구원은 어떤 연구를 수행하나요?', 
         '한국원자력연구원은 원자력 기술 연구개발을 주로 수행합니다. 특히 다목적 연구용 원자로인 "하나로"를 직접 설계 및 운영하고 있으며, 부산 기장군에도 연구용 원자로를 건설 중입니다.'),
        (gen_random_uuid(), '한국원자력연구원의 보안 등급은 어떻게 되나요?', 
         '한국원자력연구원은 국가중요시설 "가" 등급으로 지정되어 있습니다. 이는 한국 안보와 기술 유출 방지를 위한 조치입니다.');
    END IF;
END $$;

-- Setting 테이블이 비어있는지 확인하고 기본 데이터를 삽입
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM setting) THEN
        INSERT INTO setting (key, query_model, ai_model) VALUES
        (NULL, 'gpt-4o-mini', 'gpt-4o-mini');
    END IF;
END $$;
