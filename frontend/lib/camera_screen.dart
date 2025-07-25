import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

class CameraScreen extends StatefulWidget {
  final String detectionMode;
  final List<CameraDescription> cameras;

  const CameraScreen({
    required this.detectionMode,
    required this.cameras,
  });

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraController controller;
  String resultText = "Analyse en cours...";
  Timer? detectionTimer;
  bool isDetecting = false;

  @override
  void initState() {
    super.initState();
    controller = CameraController(widget.cameras[0], ResolutionPreset.medium);
    controller.initialize().then((_) {
      if (!mounted) return;
      setState(() {});
      startAutoDetection();
    });
  }

  void startAutoDetection() {
    detectionTimer = Timer.periodic(Duration(seconds: 3), (_) {
      if (!isDetecting) detectNuisible();
    });
  }

  Future<void> detectNuisible() async {
    try {
      isDetecting = true;
      final image = await controller.takePicture();
      final bytes = await image.readAsBytes();

      final url = widget.detectionMode == 'plantes'
          ? 'http://192.168.166.130:8000/detect_camera/'
          : 'http://192.168.166.130:8000/api/insectes/detect/';

      var uri = Uri.parse(url);
      var request = http.MultipartRequest('POST', uri)
        ..files.add(http.MultipartFile.fromBytes('image', bytes, filename: 'image.jpg'));

      var response = await request.send();
      var respStr = await response.stream.bytesToString();

      final json = jsonDecode(respStr);

      setState(() {
        resultText = json['message'] ?? "Réponse inconnue";
      });

      Future.delayed(Duration(seconds: 5), () {
        if (mounted) setState(() => resultText = "Analyse en cours...");
      });
    } catch (e) {
      setState(() => resultText = "Erreur : $e");
    } finally {
      isDetecting = false;
    }
  }

  @override
  void dispose() {
    controller.dispose();
    detectionTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!controller.value.isInitialized) {
      return Center(child: CircularProgressIndicator());
    }

    return Scaffold(
      appBar: AppBar(title: Text("Détection : ${widget.detectionMode}")),
      body: Stack(
        children: [
          CameraPreview(controller),
          Positioned(
            bottom: 20,
            left: 20,
            right: 20,
            child: Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.7),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                resultText,
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.white, fontSize: 16),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
