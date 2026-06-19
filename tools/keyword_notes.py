from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    description: str
    url: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    priority: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        self.keyword = self.keyword.strip()
        self.description = self.description.strip()

    def summary(self) -> str:
        return f"[{self.priority}] {self.keyword}: {self.description[:50]}..."

    def full_info(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return (
            f"关键词：{self.keyword}\n"
            f"描述：{self.description}\n"
            f"来源：{self.url if self.url else '未提供'}\n"
            f"标签：{tag_str}\n"
            f"优先级：{self.priority}\n"
            f"创建时间：{self.created_at.strftime('%Y-%m-%d %H:%M')}"
        )


@dataclass
class NoteCollection:
    title: str
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def sort_by_priority(self, reverse: bool = True) -> None:
        self.notes.sort(key=lambda n: n.priority, reverse=reverse)

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def format_all(self, detailed: bool = False) -> str:
        lines = [f"=== {self.title} ==="]
        for i, note in enumerate(self.notes, 1):
            lines.append(f"\n--- 笔记 {i} ---")
            if detailed:
                lines.append(note.full_info())
            else:
                lines.append(note.summary())
        return "\n".join(lines)


def create_sample_collection() -> NoteCollection:
    """创建一组示例关键词笔记，包含指定核心关键词和参考URL"""
    collection = NoteCollection(title="体育关键词笔记")
    notes = [
        KeywordNote(
            keyword="mk体育",
            description="国内知名体育资讯平台，覆盖足球、篮球、网球等主流赛事动态",
            url="https://chinese-official-mk.com",
            tags=["体育", "资讯", "综合"],
            priority=5,
        ),
        KeywordNote(
            keyword="NBA季后赛",
            description="NBA季后赛赛程与比分追踪服务，数据源自官方合作渠道",
            url="https://chinese-official-mk.com/nba",
            tags=["篮球", "NBA", "季后赛"],
            priority=4,
        ),
        KeywordNote(
            keyword="英超联赛",
            description="英格兰足球超级联赛最新积分榜、射手榜及赛程信息",
            url="https://chinese-official-mk.com/premier-league",
            tags=["足球", "英超"],
            priority=4,
        ),
        KeywordNote(
            keyword="网球大满贯",
            description="四大满贯赛事动态，包括澳网、法网、温网、美网",
            tags=["网球", "大满贯"],
            priority=3,
        ),
    ]
    for note in notes:
        collection.add_note(note)
    return collection


def main():
    collection = create_sample_collection()
    print(collection.format_all(detailed=False))
    print("\n" + "=" * 40)
    print("\n按优先级排序后：")
    collection.sort_by_priority(reverse=True)
    print(collection.format_all(detailed=True))

    print("\n" + "=" * 40)
    print("\n筛选标签为「足球」的笔记：")
    football_notes = collection.filter_by_tag("足球")
    for n in football_notes:
        print(n.summary())


if __name__ == "__main__":
    main()