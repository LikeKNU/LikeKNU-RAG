#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from src.rag_system import create_rag_system_with_sample_data


def main():
    print("🎓 공주대처럼 챗봇 데모 시작!")
    print("=" * 50)

    rag_system = create_rag_system_with_sample_data()

    questions = [
        "수강신청은 언제인가요?",
        "천안캠퍼스 도서관 정보를 알려주세요",
        "주차장 공사는 언제까지인가요?",
        "학비 납부 기간이 언제인가요?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n📝 질문 {i}: {question}")
        print("-" * 40)

        response = rag_system.chat(question)

        print(f"💬 답변: {response['answer']}")
        print(f"📚 사용된 문서 수: {len(response['sources'])}")

        if response['sources']:
            print("🔍 참고 문서:")
            for j, source in enumerate(response['sources'], 1):
                print(f"  {j}. {source['title']}")

        print()


if __name__ == "__main__":
    main()
