import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface Message {
    role: 'user' | 'assistant';
    content: string;
    courses?: Array<{
        course_code: string;
        reason: string;
    }>;
    timestamp?: number;
    time_taken?: number; // Time taken in seconds for assistant responses
}

interface ChatContextType {
    sessionId: string | null;
    messages: Message[];
    setSessionId: (id: string | null) => void;
    addMessage: (message: Message) => void;
    clearChat: () => void;
    initializeChat: (sessionId: string, initialResponse: any) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

const STORAGE_KEY = 'trudegree_chat';

export function ChatProvider({ children }: { children: ReactNode }) {
    const [sessionId, setSessionIdState] = useState<string | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);

    // Load from localStorage on mount
    useEffect(() => {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try {
                const data = JSON.parse(stored);
                if (data.sessionId && data.messages) {
                    setSessionIdState(data.sessionId);
                    setMessages(data.messages);
                }
            } catch (error) {
                console.error('Error loading chat from localStorage:', error);
                localStorage.removeItem(STORAGE_KEY);
            }
        }
    }, []);

    // Save to localStorage whenever sessionId or messages change
    useEffect(() => {
        if (sessionId && messages.length > 0) {
            localStorage.setItem(
                STORAGE_KEY,
                JSON.stringify({
                    sessionId,
                    messages,
                })
            );
        }
    }, [sessionId, messages]);

    const setSessionId = (id: string | null) => {
        setSessionIdState(id);
        if (!id) {
            // Clear localStorage when session is cleared
            localStorage.removeItem(STORAGE_KEY);
        }
    };

    const addMessage = (message: Message) => {
        setMessages((prev) => [
            ...prev,
            {
                ...message,
                timestamp: message.timestamp || Date.now(),
            },
        ]);
    };

    const clearChat = () => {
        setMessages([]);
        setSessionIdState(null);
        localStorage.removeItem(STORAGE_KEY);
    };

    const initializeChat = (id: string, initialResponse: any) => {
        setSessionIdState(id);
        
        const messagesToSet: Message[] = [];
        
        // Add user message if provided
        if (initialResponse.userMessage) {
            messagesToSet.push({
                role: 'user',
                content: initialResponse.userMessage,
                timestamp: Date.now(),
            });
        }
        
        // Add assistant response
        messagesToSet.push({
            role: 'assistant',
            content: initialResponse.response?.text || 'Response received',
            courses: initialResponse.response?.recommended_courses || [],
            timestamp: Date.now(),
            time_taken: initialResponse.time_taken,
        });
        
        setMessages(messagesToSet);
    };

    return (
        <ChatContext.Provider
            value={{
                sessionId,
                messages,
                setSessionId,
                addMessage,
                clearChat,
                initializeChat,
            }}
        >
            {children}
        </ChatContext.Provider>
    );
}

export function useChat() {
    const context = useContext(ChatContext);
    if (context === undefined) {
        throw new Error('useChat must be used within a ChatProvider');
    }
    return context;
}

