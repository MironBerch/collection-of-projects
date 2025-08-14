import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/weight_record.dart';

class DatabaseHelper {
  static final DatabaseHelper _instance = DatabaseHelper._internal();
  static Database? _database;

  factory DatabaseHelper() => _instance;

  DatabaseHelper._internal();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, 'weights.db');

    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDatabase,
    );
  }

  Future _createDatabase(Database db, int version) async {
    await db.execute('''
      CREATE TABLE weights(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weight REAL NOT NULL,
        date TEXT NOT NULL
      )
    ''');
  }

  Future<int> insertWeight(WeightRecord weight) async {
    final db = await database;
    return await db.insert('weights', weight.toMap());
  }

  Future<List<WeightRecord>> getWeights() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('weights', orderBy: 'date DESC');
    return List.generate(maps.length, (i) {
      return WeightRecord.fromMap(maps[i]);
    });
  }

  Future<int> updateWeight(WeightRecord weight) async {
    final db = await database;
    return await db.update(
      'weights',
      weight.toMap(),
      where: 'id = ?',
      whereArgs: [weight.id],
    );
  }

  Future<int> deleteWeight(int id) async {
    final db = await database;
    return await db.delete(
      'weights',
      where: 'id = ?',
      whereArgs: [id],
    );
  }
}