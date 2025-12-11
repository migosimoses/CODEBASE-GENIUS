"""
Codebase Genius - Data Models
Defines all nodes and edges for the system graph
"""

node file_node {
    has name: str;
    has path: str;
    has is_dir: bool;
    has language: str;
    has size: int;
    has depth: int;
}

node code_entity {
    has name: str;
    has entity_type: str;
    has file_path: str;
    has line_number: int;
    has end_line: int;
    has language: str;
    has docstring: str;
    has signature: str;
    has modifiers: list[str];
}

node code_relationship {
    has source_entity: str;
    has target_entity: str;
    has relationship_type: str;
    has source_file: str;
    has target_file: str;
    has line_number: int;
}

node repository {
    has name: str;
    has url: str;
    has path: str;
    has primary_language: str;
    has readme: str;
    has entry_points: list[str];
}

node analysis_result {
    has repo_name: str;
    has total_files: int;
    has total_entities: int;
    has entity_count_by_type: dict;
    has languages_found: list[str];
    has analysis_timestamp: str;
}

node documentation {
    has title: str;
    has content: str;
    has repo_name: str;
    has generated_at: str;
    has sections: dict;
}

edge has_child {
    has order: int;
}

edge has_entity {
    has scope: str;
}

edge entity_calls {
    has line_number: int;
    has is_direct: bool;
}

edge references {
    has reference_type: str;
}

edge generated_from {
    has sections_included: list[str];
}
