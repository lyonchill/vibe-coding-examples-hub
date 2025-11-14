-- Supabase 數據表結構（可選）
-- 如果使用 Supabase 存儲數據，運行此 SQL 創建表

CREATE TABLE IF NOT EXISTS examples (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    project_name TEXT,
    project_summary TEXT,
    project_evidence TEXT,
    ai_tools_used TEXT[],
    category_tags TEXT[],
    source_platform TEXT NOT NULL,
    original_url TEXT NOT NULL UNIQUE,
    creator_name TEXT,
    creator_link TEXT,
    thumbnail_url TEXT,
    date_added TIMESTAMP DEFAULT NOW(),
    relevance_score INTEGER DEFAULT 0,
    build_complexity TEXT,
    is_no_code_low_code BOOLEAN DEFAULT FALSE,
    primary_category TEXT,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 創建索引以優化查詢
CREATE INDEX IF NOT EXISTS idx_source_platform ON examples(source_platform);
CREATE INDEX IF NOT EXISTS idx_primary_category ON examples(primary_category);
CREATE INDEX IF NOT EXISTS idx_relevance_score ON examples(relevance_score DESC);
CREATE INDEX IF NOT EXISTS idx_view_count ON examples(view_count DESC);

-- 更新時間戳觸發器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_examples_updated_at BEFORE UPDATE ON examples
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

