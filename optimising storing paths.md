# How I optimised path searching operations
Our whole system is dependent on searching paths and directories of whether we need to watch the path or to ignore it.
> We are not setting up watchers for individual files rather for a whole directory at each levels. But individual files can be ignored

### Where we are actually using path
1. Adding paths to watch
2. ignoring paths during watching
Isn't that simple storing lists and sets?
```bash
core_path = WatcherPath(
    "/home/arnab/Desktop/system-implementations/py-mon/src/core", ignore=["cache.txt","__pycache__",".venv"]
)
watcher = Watcher().add_path(core_path, test_path).add_event(RELOAD_EVENTS)
```

* We can definitely do this. For each paths we can search for all the ignore paths and then determine whether that is ignored or not.
A typical `O(n*m)` solution

### Solving this with trie data structure

### Current Check (O(N * M))
Currently, for each path in `os.walk()`, we iterate over all ignore paths and check if it starts with an ignored directory.

```python
for dirpath, dirnames, _ in os.walk(base_path):
    for ignore_path in ignore_list:  # Loop over all ignore paths
        if dirpath.startswith(ignore_path):  # Check if it's ignored
            print(f"Ignored: {dirpath}")
```

### Issue
For **N** directories and **M** ignore paths, we check every directory against every ignore path → **O(N * M)** time complexity.

---

## 🚀 Trie-Based Approach (O(N * L))
### How Trie Improves This?
A **Trie** organizes ignored paths hierarchically, allowing fast prefix lookups instead of scanning all ignore paths.

* Instead of checking each path against all ignored paths,  
* We traverse the **Trie** once for each path, reducing comparisons.

---

### 📌 Example
#### 📂 Given Directory Structure
```
/root/
 ├── logs/
 │   ├── error.log
 │   └── access.log
 ├── src/
 │   ├── test/
 │   │   ├── test1.py
 │   │   └── test2.py
 │   └── temp/
 │       └── temp.txt
 └── data/
```
#### Ignore Paths
```
/root/logs
/root/src/test
/root/src/temp
```

---

### Current Approach (O(N * M))
For every directory, we compare it against each ignore path:

```plaintext
Checking /root/logs  -> Compare with logs (Ignored ✅)
Checking /root/src/test -> Compare with logs ❌, test ✅ (Ignored ✅)
Checking /root/src/temp -> Compare with logs ❌, test ❌, temp ✅ (Ignored ✅)
Checking /root/data  -> Compare with logs ❌, test ❌, temp ❌ (Not Ignored ✅)
```
**Every directory is checked against all ignored paths!**

---

### Trie-Based Approach (O(N * L))
#### 📂 Trie Structure
```
(root)
 ├── logs (*)
 └── src
     ├── test (*)
     └── temp (*)
```

#### 🔍 Traversal Using Trie
Instead of checking each directory against all ignore paths, we traverse:

```plaintext
Checking /root/logs -> logs is in Trie (Ignored ✅)
Checking /root/src/test -> src → test is in Trie (Ignored ✅)
Checking /root/src/temp -> src → temp is in Trie (Ignored ✅)
Checking /root/data -> Not in Trie (Not Ignored ✅)
```
✅ **Each directory is checked in O(L) time (L = path depth), avoiding multiple comparisons.**

---

### Complexity Comparison
| Approach       | Comparisons Per Directory | Worst-Case Complexity |
|---------------|-------------------------|----------------------|
| **Brute Force** | M (All ignore paths)     | O(N * M)             |
| **Trie Lookup** | L (Path depth)           | O(N * L)             |

🚀 **Trie reduces comparisons drastically, making lookups much faster!**
