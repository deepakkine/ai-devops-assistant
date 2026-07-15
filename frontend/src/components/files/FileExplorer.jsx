import { useMemo, useState } from "react";

function buildTree(files) {
  const root = {};

  files.forEach((file) => {
    const parts = file.split("/");

    let current = root;

    parts.forEach((part, index) => {
      if (!current[part]) {
        current[part] = {
          name: part,
          children: {},
          path: parts.slice(0, index + 1).join("/"),
          isFile: index === parts.length - 1,
        };
      }

      current = current[part].children;
    });
  });

  return Object.values(root);
}

function TreeNode({
  node,
  selectedFile,
  onSelect,
  level,
  expanded,
  toggleFolder,
  search,
}) {
  if (node.isFile) {
    if (
      search &&
      !node.path
        .toLowerCase()
        .includes(search.toLowerCase())
    ) {
      return null;
    }

    const selected = selectedFile === node.path;

    return (
      <button
        onClick={() => onSelect(node.path)}
        className={`flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-sm transition ${
          selected
            ? "bg-blue-600 text-white shadow"
            : "text-slate-700 hover:bg-slate-200 dark:text-slate-300 dark:hover:bg-slate-800"
        }`}
        style={{
          paddingLeft: `${level * 18 + 12}px`,
        }}
      >
        <span>📄</span>
        <span className="truncate">
          {node.name}
        </span>
      </button>
    );
  }

  const children = Object.values(node.children)
    .sort((a, b) => {
      if (a.isFile === b.isFile) {
        return a.name.localeCompare(b.name);
      }

      return a.isFile ? 1 : -1;
    })
    .filter((child) => {
      if (!search) return true;

      return child.path
        .toLowerCase()
        .includes(search.toLowerCase());
    });

  if (search && children.length === 0) {
    return null;
  }

  const isExpanded = search
    ? true
    : expanded[node.path] ?? true;

  return (
    <div>
      <button
        onClick={() => toggleFolder(node.path)}
        className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-sm font-semibold text-slate-600 transition hover:bg-slate-200 dark:text-slate-300 dark:hover:bg-slate-800"
        style={{
          paddingLeft: `${level * 18 + 12}px`,
        }}
      >
        <span className="w-4">
          {isExpanded ? "▼" : "▶"}
        </span>

        <span>
          {isExpanded ? "📂" : "📁"}
        </span>

        <span className="truncate">
          {node.name}
        </span>
      </button>

      {isExpanded &&
        children.map((child) => (
          <TreeNode
            key={child.path}
            node={child}
            selectedFile={selectedFile}
            onSelect={onSelect}
            level={level + 1}
            expanded={expanded}
            toggleFolder={toggleFolder}
            search={search}
          />
        ))}
    </div>
  );
}

export default function FileExplorer({
  files,
  selectedFile,
  onSelect,
}) {
  const [expanded, setExpanded] =
    useState({});

  const [search, setSearch] =
    useState("");

  const tree = useMemo(
    () => buildTree(files),
    [files]
  );

  function toggleFolder(path) {
    setExpanded((prev) => ({
      ...prev,
      [path]: !(prev[path] ?? true),
    }));
  }

  return (
    <div className="flex h-full flex-col bg-white transition-colors dark:bg-slate-900">
      <div className="sticky top-0 space-y-3 border-b border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-900">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
          📁 Repository Files
        </h2>

        <div className="relative">
          <input
            type="text"
            placeholder="Search files..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
            className="w-full rounded-lg border border-slate-300 bg-slate-50 px-4 py-2 text-sm outline-none transition focus:border-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
          />

          {search && (
            <button
              onClick={() => setSearch("")}
              className="absolute right-3 top-2 text-slate-500 hover:text-red-500"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        {tree
          .sort((a, b) => {
            if (a.isFile === b.isFile) {
              return a.name.localeCompare(
                b.name
              );
            }

            return a.isFile ? 1 : -1;
          })
          .map((node) => (
            <TreeNode
              key={node.path}
              node={node}
              selectedFile={selectedFile}
              onSelect={onSelect}
              level={0}
              expanded={expanded}
              toggleFolder={toggleFolder}
              search={search}
            />
          ))}
      </div>
    </div>
  );
}