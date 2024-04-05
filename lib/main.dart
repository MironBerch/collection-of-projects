import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:path/path.dart' as p;
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'package:path_provider/path_provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  if (Platform.isLinux || Platform.isWindows) {
    sqfliteFfiInit();
    databaseFactory = databaseFactoryFfi;
  }
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Media Filter',
      theme: ThemeData(primarySwatch: Colors.blue),
      initialRoute: '/',
      routes: {
        '/': (context) => const HomeScreen(),
        '/create': (context) => const ProcessCreationScreen(),
        '/filter': (context) => FilterScreen(
              processId: ModalRoute.of(context)!.settings.arguments as int,
            ),
        '/delete': (context) => const DeletionScreen(),
      },
    );
  }
}

class AppDatabase {
  static final AppDatabase _instance = AppDatabase._();
  static Database? _database;

  AppDatabase._();

  factory AppDatabase() => _instance;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB();
    return _database!;
  }

  Future<Database> _initDB() async {
    Directory dir = await getApplicationDocumentsDirectory();
    String path = p.join(dir.path, 'media_filter.db');
    return openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE processes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            folder_path TEXT
          )
        ''');
        await db.execute('''
          CREATE TABLE media_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process_id INTEGER,
            file_path TEXT,
            status INTEGER DEFAULT 0
          )
        ''');
      },
    );
  }
}

class Process {
  final int id;
  final String name;
  final String folderPath;

  const Process({
    required this.id,
    required this.name,
    required this.folderPath,
  });
}

class MediaFile {
  final int id;
  final int processId;
  final String filePath;
  final int status;

  const MediaFile({
    required this.id,
    required this.processId,
    required this.filePath,
    required this.status,
  });
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Process> _processes = [];

  @override
  void initState() {
    super.initState();
    _loadProcesses();
  }

  Future<void> _loadProcesses() async {
    final db = await AppDatabase().database;
    final List<Map<String, dynamic>> maps = await db.query('processes');
    if (!mounted) return;
    setState(() {
      _processes = List.generate(maps.length, (i) => Process(
            id: maps[i]['id'],
            name: maps[i]['name'],
            folderPath: maps[i]['folder_path'],
          ));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Processes'),
        actions: [
          IconButton(
            icon: const Icon(Icons.delete),
            onPressed: () => Navigator.pushNamed(context, '/delete'),
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: _processes.length,
        itemBuilder: (context, index) => ListTile(
          title: Text(_processes[index].name),
          subtitle: Text(_processes[index].folderPath),
          onTap: () => Navigator.pushNamed(
            context,
            '/filter',
            arguments: _processes[index].id,
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.add),
        onPressed: () => Navigator.pushNamed(context, '/create'),
      ),
    );
  }
}

class ProcessCreationScreen extends StatefulWidget {
  const ProcessCreationScreen({Key? key}) : super(key: key);

  @override
  _ProcessCreationScreenState createState() => _ProcessCreationScreenState();
}

class _ProcessCreationScreenState extends State<ProcessCreationScreen> {
  final _nameController = TextEditingController();
  String? _folderPath;

  Future<void> _pickFolder() async {
    String? path = await FilePicker.platform.getDirectoryPath();
    if (path != null && mounted) setState(() => _folderPath = path);
  }

  bool _isImageOrVideo(String path) {
    final ext = p.extension(path).toLowerCase();
    return ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi'].contains(ext);
  }

  Future<void> _saveProcess() async {
    if (_nameController.text.isEmpty || _folderPath == null) return;

    final db = await AppDatabase().database;
    final processId = await db.insert('processes', {
      'name': _nameController.text,
      'folder_path': _folderPath,
    });

    final dir = Directory(_folderPath!);
    List<FileSystemEntity> files = await dir.list(recursive: true).toList();
    
    for (var file in files) {
      if (file is File && _isImageOrVideo(file.path)) {
        await db.insert('media_files', {
          'process_id': processId,
          'file_path': file.path,
          'status': 0,
        });
      }
    }

    if (!mounted) return;
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('New Process')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(labelText: 'Process Name'),
            ),
            ElevatedButton(
              onPressed: _pickFolder,
              child: const Text('Select Folder'),
            ),
            Text(_folderPath ?? 'No folder selected'),
            ElevatedButton(
              onPressed: _saveProcess,
              child: const Text('Save Process'),
            ),
          ],
        ),
      ),
    );
  }
}

class FilterScreen extends StatefulWidget {
  final int processId;

  const FilterScreen({
    Key? key,
    required this.processId,
  }) : super(key: key);

  @override
  _FilterScreenState createState() => _FilterScreenState();
}

class _FilterScreenState extends State<FilterScreen> {
  List<MediaFile> _mediaFiles = [];
  int _currentIndex = 0;
  int _total = 0;
  int _processed = 0;

  Future<void> _loadMediaFiles() async {
    final db = await AppDatabase().database;
    final List<Map<String, dynamic>> maps = await db.query(
      'media_files',
      where: 'process_id = ? AND status = 0',
      whereArgs: [widget.processId],
    );

    if (!mounted) return;
    setState(() {
      _mediaFiles = List.generate(maps.length, (i) => MediaFile(
            id: maps[i]['id'],
            processId: maps[i]['process_id'],
            filePath: maps[i]['file_path'],
            status: maps[i]['status'],
          ));
      _total = _mediaFiles.length;
      _processed = 0;
    });
  }

  Future<void> _updateStatus(int status) async {
    if (_currentIndex >= _mediaFiles.length) return;

    final db = await AppDatabase().database;
    await db.update(
      'media_files',
      {'status': status},
      where: 'id = ?',
      whereArgs: [_mediaFiles[_currentIndex].id],
    );

    if (!mounted) return;
    setState(() {
      _currentIndex++;
      _processed++;
    });
  }

  @override
  void initState() {
    super.initState();
    _loadMediaFiles();
  }

    @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Filtering: $_processed/$_total'),
      ),
      body: Column(
        children: [
          // Основное содержимое с изображением
          Expanded(
            child: _currentIndex < _mediaFiles.length
                ? Center(
                    child: SingleChildScrollView(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Image.file(
                            File(_mediaFiles[_currentIndex].filePath),
                            errorBuilder: (context, error, stackTrace) {
                              return const Text('Не удалось загрузить изображение');
                            },
                          ),
                          const SizedBox(height: 20),
                        ],
                      ),
                    ),
                  )
                : const Center(child: Text('All files processed!')),
          ),
          // Фиксированная панель с кнопками внизу
          Container(
            padding: const EdgeInsets.all(16),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: _currentIndex < _mediaFiles.length 
                      ? () => _updateStatus(2)
                      : null,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red,
                    minimumSize: const Size(120, 50),
                  ),
                  child: const Text('Dislike'),
                ),
                ElevatedButton(
                  onPressed: _currentIndex < _mediaFiles.length 
                      ? () => _updateStatus(1)
                      : null,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    minimumSize: const Size(120, 50),
                  ),
                  child: const Text('Like'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class DeletionScreen extends StatelessWidget {
  const DeletionScreen({Key? key}) : super(key: key);

  Future<List<MediaFile>> _getFilesToDelete() async {
    final db = await AppDatabase().database;
    final List<Map<String, dynamic>> maps = await db.query(
      'media_files',
      where: 'status = 2',
    );
    return List.generate(maps.length, (i) => MediaFile(
          id: maps[i]['id'],
          processId: maps[i]['process_id'],
          filePath: maps[i]['file_path'],
          status: maps[i]['status'],
        ));
  }

  Future<void> _deleteFiles(List<MediaFile> files) async {
    for (var file in files) {
      try {
        final f = File(file.filePath);
        if (await f.exists()) {
          await f.delete();
        }
      } catch (e) {
        debugPrint('Error deleting file: $e');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Files to Delete')),
      body: FutureBuilder<List<MediaFile>>(
        future: _getFilesToDelete(),
        builder: (context, snapshot) {
          if (!snapshot.hasData) return const CircularProgressIndicator();
          final files = snapshot.data!;
          return ListView.builder(
            itemCount: files.length,
            itemBuilder: (context, index) => ListTile(
              title: Text(files[index].filePath),
              trailing: const Icon(Icons.delete),
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.delete_forever),
        onPressed: () async {
          final files = await _getFilesToDelete();
          await _deleteFiles(files);
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Deleted ${files.length} files')),
          );
        },
      ),
    );
  }
}