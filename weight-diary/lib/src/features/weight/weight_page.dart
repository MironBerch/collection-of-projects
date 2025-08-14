import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../models/weight_record.dart';
import '../../services/database_helper.dart';
import './add_edit_weight_page.dart';

class WeightPage extends StatefulWidget {
  const WeightPage({super.key});

  @override
  State<WeightPage> createState() => _WeightPageState();
}

class _WeightPageState extends State<WeightPage> {
  final DatabaseHelper _dbHelper = DatabaseHelper();
  List<WeightRecord> _weights = [];

  @override
  void initState() {
    super.initState();
    _loadWeights();
  }

  Future<void> _loadWeights() async {
    final weights = await _dbHelper.getWeights();
    setState(() {
      _weights = weights;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _weights.isEmpty
          ? const Center(child: Text('No weight records yet'))
          : ListView.builder(
              itemCount: _weights.length,
              itemBuilder: (context, index) {
                final weight = _weights[index];
                return ListTile(
                  title: Text('${weight.weight} kg'),
                  subtitle: Text(DateFormat('yyyy-MM-dd HH:mm').format(weight.date)),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.edit),
                        onPressed: () => _editWeight(context, weight),
                      ),
                      IconButton(
                        icon: const Icon(Icons.delete),
                        onPressed: () => _deleteWeight(weight.id!),
                      ),
                    ],
                  ),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _addWeight(context),
        tooltip: 'Add weight record',
        child: const Icon(Icons.add),
      ),
    );
  }

  Future<void> _addWeight(BuildContext context) async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const AddEditWeightPage()),
    );
    
    if (result == true) {
      _loadWeights();
    }
  }

  Future<void> _editWeight(BuildContext context, WeightRecord weight) async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => AddEditWeightPage(weight: weight),
      ),
    );
    
    if (result == true) {
      _loadWeights();
    }
  }

  Future<void> _deleteWeight(int id) async {
    await _dbHelper.deleteWeight(id);
    _loadWeights();
  }
}