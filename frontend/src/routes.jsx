import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from './layouts/AppLayout'
import ProtectedRoute from './components/ProtectedRoute'
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import SelectYear from './pages/SelectYear'
import SelectSemester from './pages/SelectSemester'
import SelectModule from './pages/SelectModule'
import ModuleHome from './pages/ModuleHome'
import Courses from './pages/Courses'
import QuizSetup from './pages/QuizSetup'
import Quiz from './pages/Quiz'
import Stats from './pages/Stats'
import Todos from './pages/Todos'
import { PlaceholderPage } from './pages/WorkspacePages'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route index element={<Home />} />
          <Route path="years" element={<SelectYear />} />
          <Route path="years/:yearId/semesters" element={<SelectSemester />} />
          <Route path="semesters/:semesterId/modules" element={<SelectModule />} />
          <Route path="modules/:moduleId" element={<ModuleHome />} />
          <Route path="modules/:moduleId/revision" element={<Courses />} />
          <Route path="modules/:moduleId/stats" element={<Stats />} />
          <Route path="courses/:courseId/quiz/setup" element={<QuizSetup />} />
          <Route path="quiz" element={<Quiz />} />
          <Route path="todos" element={<Todos />} />
          <Route path="courses" element={<Courses />} />
          <Route path="schedule" element={<PlaceholderPage />} />
          <Route path="progress" element={<PlaceholderPage />} />
        </Route>
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
