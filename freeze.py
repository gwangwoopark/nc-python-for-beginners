# freeze.py
from app import app
from flask_frozen import Freezer

# Frozen-Flask 설정
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True

freezer = Freezer(app)

# 동적 라우트를 위한 URL generator
# /search/<keyword> 라우트를 위한 generator
@freezer.register_generator
def search():
    keywords = ["python", "javascript", "java"]
    print(f"\nGenerating search pages for keywords: {keywords}")
    for keyword in keywords:
        print(f"  - /search/{keyword}")
        yield {'keyword': keyword}


if __name__ == '__main__':
    print("Starting freeze process...")
    
    # 모든 URL 확인
    urls = list(freezer.all_urls())
    print(f"\nAll URLs to be frozen ({len(urls)} total):")
    for url in urls:
        print(f"  {url}")
    
    print("\nFreezing...")
    freezer.freeze()
    print("\n✅ Freeze completed! Check the 'build' directory.")

