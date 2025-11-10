import { useState, useEffect, useRef, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useChat } from '@/context/chatContext';
import DefaultLayout from '@/layouts/default';
import { Button } from '@heroui/button';
import { Card, CardBody, CardHeader } from '@heroui/card';
import { Switch } from '@heroui/switch';
import axios from 'axios';
import { title } from '@/components/primitives';
import LoadingProgress from '@/components/LoadingProgress';
import ReactMarkdown from 'react-markdown';

const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function ChatPage() {
    const navigate = useNavigate();
    const { sessionId, messages, addMessage, clearChat } = useChat();
    const [input, setInput] = useState('');
    const [isSending, setIsSending] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isLongPlanningMode, setIsLongPlanningMode] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const coursesEndRef = useRef<HTMLDivElement>(null);

    // Get the latest recommended courses from the most recent assistant message
    const latestCourses = useMemo(() => {
        // Find the most recent assistant message with courses
        for (let i = messages.length - 1; i >= 0; i--) {
            const message = messages[i];
            if (
                message.role === 'assistant' &&
                message.courses &&
                Array.isArray(message.courses) &&
                message.courses.length > 0
            ) {
                return message.courses;
            }
        }
        return [];
    }, [messages]);

    // Scroll to bottom when messages change
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Scroll courses into view when they update
    useEffect(() => {
        if (latestCourses.length > 0) {
            setTimeout(() => {
                coursesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        }
    }, [latestCourses]);

    // Redirect if no session
    useEffect(() => {
        if (!sessionId) {
            navigate('/');
        }
    }, [sessionId, navigate]);

    const handleSend = async () => {
        if (!input.trim() || !sessionId || isSending) return;

        const userMessage = input.trim();
        setInput('');
        setError(null);
        setIsSending(true);

        // Add user message to UI immediately
        addMessage({
            role: 'user',
            content: userMessage,
        });

        try {
            const formData = new FormData();
            formData.append('session_id', sessionId);
            formData.append('message', userMessage);
            formData.append(
                'is_long_planning_mode',
                String(isLongPlanningMode)
            );

            const response = await axios.post(
                `${API_BASE_URL}/api/chat`,
                formData
            );

            // Add assistant response
            addMessage({
                role: 'assistant',
                content: response.data.response?.text || 'Response received',
                courses: response.data.response?.recommended_courses || [],
                time_taken: response.data.time_taken,
            });
        } catch (err) {
            setError(
                err instanceof Error ? err.message : 'Failed to send message'
            );
            console.error('Error sending message:', err);
        } finally {
            setIsSending(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    if (!sessionId) {
        return null; // Will redirect
    }

    return (
        <DefaultLayout>
            <div className="flex flex-col min-h-[calc(100vh-200px)] max-w-6xl mx-auto px-4 py-6">
                {/* Header */}
                <div className="flex items-center justify-between mb-4">
                    <h1 className={title({ size: 'md' })}>
                        Chat with TruDegree
                    </h1>
                    <Button
                        variant="light"
                        color="danger"
                        size="sm"
                        onPress={clearChat}
                        isDisabled={isSending}
                    >
                        Clear Chat
                    </Button>
                </div>

                <div className="flex gap-6 flex-col lg:flex-row">
                    {/* Left: Messages */}
                    <div className="flex-1 flex flex-col min-h-0">
                        <div className="flex-1 overflow-y-auto mb-4 space-y-4 max-h-[60vh]">
                            {messages.length === 0 ? (
                                <div className="text-center text-default-500 py-8">
                                    No messages yet. Start the conversation!
                                </div>
                            ) : (
                                messages.map((message, index) => (
                                    <div
                                        key={index}
                                        className={`flex ${
                                            message.role === 'user'
                                                ? 'justify-end'
                                                : 'justify-start'
                                        }`}
                                    >
                                        <Card
                                            className={`max-w-[80%] ${
                                                message.role === 'user'
                                                    ? 'bg-secondary-100'
                                                    : ''
                                            }`}
                                            shadow="sm"
                                        >
                                            <CardBody className="p-4">
                                                <div className="markdown-content">
                                                    <ReactMarkdown
                                                        components={{
                                                            h1: ({
                                                                children,
                                                            }) => (
                                                                <h1 className="text-2xl font-bold mb-2 mt-4 first:mt-0">
                                                                    {children}
                                                                </h1>
                                                            ),
                                                            h2: ({
                                                                children,
                                                            }) => (
                                                                <h2 className="text-xl font-bold mb-2 mt-4 first:mt-0">
                                                                    {children}
                                                                </h2>
                                                            ),
                                                            h3: ({
                                                                children,
                                                            }) => (
                                                                <h3 className="text-lg font-semibold mb-2 mt-3 first:mt-0">
                                                                    {children}
                                                                </h3>
                                                            ),
                                                            p: ({
                                                                children,
                                                            }) => (
                                                                <p className="mb-2 last:mb-0">
                                                                    {children}
                                                                </p>
                                                            ),
                                                            ul: ({
                                                                children,
                                                            }) => (
                                                                <ul className="list-disc list-inside mb-2 space-y-1">
                                                                    {children}
                                                                </ul>
                                                            ),
                                                            ol: ({
                                                                children,
                                                            }) => (
                                                                <ol className="list-decimal list-inside mb-2 space-y-1">
                                                                    {children}
                                                                </ol>
                                                            ),
                                                            li: ({
                                                                children,
                                                            }) => (
                                                                <li className="ml-2">
                                                                    {children}
                                                                </li>
                                                            ),
                                                            strong: ({
                                                                children,
                                                            }) => (
                                                                <strong className="font-semibold">
                                                                    {children}
                                                                </strong>
                                                            ),
                                                            em: ({
                                                                children,
                                                            }) => (
                                                                <em className="italic">
                                                                    {children}
                                                                </em>
                                                            ),
                                                            code: ({
                                                                children,
                                                            }) => (
                                                                <code className="bg-default-100 px-1.5 py-0.5 rounded text-sm font-mono">
                                                                    {children}
                                                                </code>
                                                            ),
                                                        }}
                                                    >
                                                        {message.content}
                                                    </ReactMarkdown>
                                                </div>
                                                {message.role === 'assistant' &&
                                                    message.time_taken && (
                                                        <div className="mt-2 text-xs text-default-500 italic">
                                                            Generated in{' '}
                                                            {typeof message.time_taken ===
                                                            'number'
                                                                ? message.time_taken.toFixed(
                                                                      1
                                                                  )
                                                                : message.time_taken}
                                                            s
                                                        </div>
                                                    )}
                                            </CardBody>
                                        </Card>
                                    </div>
                                ))
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Loading Progress */}
                        <LoadingProgress
                            mode="chat"
                            isLongPlanning={isLongPlanningMode}
                            isVisible={isSending}
                        />

                        {/* Error message */}
                        {error && (
                            <div className="mb-4 p-3 rounded-lg bg-danger-50 text-danger text-sm">
                                {error}
                            </div>
                        )}

                        {/* Planning Mode Toggle */}
                        <div className="flex items-center justify-between p-3 rounded-lg bg-default-100 mb-3">
                            <div className="flex flex-col">
                                <span className="text-sm font-semibold">
                                    {isLongPlanningMode
                                        ? 'Long Planning Mode'
                                        : 'Normal Tasks Mode'}
                                </span>
                                <span className="text-xs text-default-600">
                                    {isLongPlanningMode
                                        ? 'Comprehensive planning, longer wait time (2-3 minutes)'
                                        : 'Quick Q&A and short-term planning, shorter wait time (40-70 seconds)'}
                                </span>
                            </div>
                            <Switch
                                isSelected={isLongPlanningMode}
                                onValueChange={setIsLongPlanningMode}
                                color="secondary"
                                isDisabled={isSending}
                            />
                        </div>

                        {/* Input area */}
                        <div className="flex gap-2">
                            <textarea
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Type your message..."
                                rows={3}
                                disabled={isSending}
                                className="flex-1 px-3 py-2 text-sm bg-transparent border border-default-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary focus:border-transparent resize-none disabled:opacity-50 disabled:cursor-not-allowed"
                            />
                            <Button
                                color="secondary"
                                onPress={handleSend}
                                isDisabled={!input.trim() || isSending}
                                isLoading={isSending}
                                className="self-end"
                                variant="shadow"
                            >
                                Send
                            </Button>
                        </div>

                        {/* Catalog Link Button */}
                        <div className="mt-4 pt-4 border-t border-default-200">
                            <Button
                                variant="shadow"
                                color="secondary"
                                size="sm"
                                as="a"
                                href="http://catalog.truman.edu/"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-sm font-medium P-5"
                                startContent={
                                    <span className="text-lg">📚</span>
                                }
                            >
                                View Official Catalog for More Information
                            </Button>
                        </div>
                    </div>

                    {/* Right: Recommended Courses Section */}
                    {latestCourses.length > 0 && (
                        <div className="lg:w-96 lg:sticky lg:top-4 lg:h-fit lg:max-h-[80vh] lg:overflow-y-auto">
                            <div className="mb-4">
                                <h2 className="text-lg font-semibold mb-3">
                                    Recommended Courses
                                </h2>
                                <div className="space-y-3">
                                    {latestCourses.map((course, index) => (
                                        <Card
                                            key={index}
                                            className="hover:shadow-md transition-shadow"
                                            shadow="sm"
                                            isHoverable
                                        >
                                            <CardHeader className="pb-2">
                                                <div className="font-bold text-lg text-secondary">
                                                    {course.course_code}
                                                </div>
                                            </CardHeader>
                                            <CardBody className="pt-0">
                                                <p className="text-sm text-default-600">
                                                    {course.reason}
                                                </p>
                                            </CardBody>
                                        </Card>
                                    ))}
                                </div>
                                <div ref={coursesEndRef} />
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </DefaultLayout>
    );
}

