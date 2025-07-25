import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'camera_screen.dart';

List<CameraDescription>? cameras;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  cameras = await availableCameras();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AGRIX',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.green,
        fontFamily: 'Roboto',
        scaffoldBackgroundColor: Colors.white,
      ),
      home: SplashScreen(),
    );
  }
}

// 🌾 SplashScreen animé
class SplashScreen extends StatefulWidget {
  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  bool _showText = false;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: Duration(seconds: 2),
    );

    _scaleAnimation = Tween<double>(begin: 3.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOut),
    );

    _controller.forward().then((_) {
      setState(() {
        _showText = true;
      });
    });

    _navigateToHome();
  }

  _navigateToHome() async {
    await Future.delayed(Duration(seconds: 4));
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => HomePage()),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ScaleTransition(
              scale: _scaleAnimation,
              child: Image.asset(
                'assets/fares.png',
                width: 150,
                height: 150,
              ),
            ),
            SizedBox(height: 20),
            if (_showText)
              Text(
                'AGRIX',
                style: TextStyle(
                  fontSize: 48,
                  fontWeight: FontWeight.bold,
                  color: Colors.green[800],
                  letterSpacing: 2,
                ),
              ),
          ],
        ),
      ),
    );
  }
}

// 🌿 Page d’accueil avec BottomNavigationBar stylée
class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _selectedIndex = 0;

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });

    if (index == 0) {
      _navigateToDetection('plantes');
    } else if (index == 1) {
      _navigateToDetection('insectes');
    }
  }

  void _navigateToDetection(String mode) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => CameraScreen(
          detectionMode: mode,
          cameras: cameras!,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Bienvenue dans AGRIX"),
        centerTitle: true,
        backgroundColor: Colors.green[700],
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.eco, color: Colors.green[600], size: 80),
              SizedBox(height: 20),
              Text(
                'Détection intelligente pour l’agriculture',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.w500,
                  color: Colors.grey[800],
                ),
              ),
              SizedBox(height: 10),
              Text(
                'Analysez vos plantes et détectez les insectes nuisibles facilement avec la caméra.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey[600]),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Colors.green[50],
        selectedItemColor: Colors.green[800],
        unselectedItemColor: Colors.green[400],
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.local_florist),
            label: 'Plantes',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.bug_report),
            label: 'Insectes',
          ),
        ],
      ),
    );
  }
}
