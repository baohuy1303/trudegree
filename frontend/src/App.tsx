import { Route, Routes } from "react-router-dom";

import IndexPage from "@/pages/index";
import ChatPage from '@/pages/chat';

function App() {
    return (
        <Routes>
            <Route element={<IndexPage />} path="/" />
            <Route element={<ChatPage />} path="/chat" />
        </Routes>
    );
}

export default App;
