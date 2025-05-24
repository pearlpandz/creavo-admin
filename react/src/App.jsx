import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TanstackProvider from './tanstack-query/Provider';
import EditPage from './pages/Edit';
import CreatePage from './pages/Create';
import ListPage from './pages/List';
import { ToastContainer } from 'react-toastify';

import './App.css'

function App() {
    return (
        <TanstackProvider>
            <Router>
                <Routes>
                    <Route index element={<ListPage />} />
                    <Route path='create' element={<CreatePage />} />
                    <Route path='edit/:templateId' element={<EditPage />} />
                </Routes>
            </Router>
            <ToastContainer />
        </TanstackProvider>
    );
}

export default App;