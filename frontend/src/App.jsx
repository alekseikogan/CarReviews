import { Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import CarDetailPage from './pages/CarDetailPage';
import AboutPage from './pages/AboutPage';
import MarksPage from './pages/MarksPage';
import BodiesPage from './pages/BodiesPage';

export default function App() {
  return (
    <div className="app">
      <Header />
      <main className="main">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/marks" element={<MarksPage />} />
          <Route path="/bodies" element={<BodiesPage />} />
          <Route path="/cars/:slug" element={<CarDetailPage />} />
          <Route path="/about" element={<AboutPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
