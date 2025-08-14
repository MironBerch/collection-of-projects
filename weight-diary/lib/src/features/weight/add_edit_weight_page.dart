import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../models/weight_record.dart';
import '../../services/database_helper.dart';

class AddEditWeightPage extends StatefulWidget {
  final WeightRecord? weight;

  const AddEditWeightPage({super.key, this.weight});

  @override
  State<AddEditWeightPage> createState() => _AddEditWeightPageState();
}

class _AddEditWeightPageState extends State<AddEditWeightPage> {
  final _formKey = GlobalKey<FormState>();
  final _weightController = TextEditingController();
  DateTime _selectedDate = DateTime.now();
  final _dbHelper = DatabaseHelper();

  @override
  void initState() {
    super.initState();
    if (widget.weight != null) {
      _weightController.text = widget.weight!.weight.toString();
      _selectedDate = widget.weight!.date;
    }
  }

  @override
  void dispose() {
    _weightController.dispose();
    super.dispose();
  }

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime(2000),
      lastDate: DateTime.now(),
    );
    if (picked != null && picked != _selectedDate) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  Future<void> _saveWeight() async {
    if (_formKey.currentState!.validate()) {
      try {
        final weight = WeightRecord(
          id: widget.weight?.id,
          weight: double.parse(_weightController.text),
          date: _selectedDate,
        );

        final dbHelper = DatabaseHelper();
        if (weight.id == null) {
          await dbHelper.insertWeight(weight);
        } else {
          await dbHelper.updateWeight(weight);
        }

        if (mounted) {
          Navigator.pop(context, true);
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Ошибка: ${e.toString()}')),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.weight == null ? 'Добавить вес' : 'Редактировать вес'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _weightController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Вес (кг)',
                  hintText: 'Например: 68.5',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) return 'Введите вес';
                  if (double.tryParse(value) == null) return 'Неверный формат';
                  return null;
                },
              ),
              const SizedBox(height: 20),
              Row(
                children: [
                  Text(
                    DateFormat('dd.MM.yyyy').format(_selectedDate),
                    style: const TextStyle(fontSize: 16),
                  ),
                  const SizedBox(width: 20),
                  ElevatedButton(
                    onPressed: () => _selectDate(context),
                    child: const Text('Изменить дату'),
                  ),
                ],
              ),
              const SizedBox(height: 80), // Отступ для bottom sheet
            ],
          ),
        ),
      ),
      bottomSheet: Container(
        color: Theme.of(context).scaffoldBackgroundColor,
        padding: const EdgeInsets.all(16.0),
        child: SizedBox(
          width: double.infinity,
          child: ElevatedButton(
            onPressed: _saveWeight,
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            child: const Text(
              'Сохранить',
              style: TextStyle(fontSize: 18),
            ),
          ),
        ),
      ),
    );
  }
}