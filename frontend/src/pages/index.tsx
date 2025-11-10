import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { title, subtitle } from '@/components/primitives';
import DefaultLayout from '@/layouts/default';
import { Card, CardHeader, CardBody } from '@heroui/card';
import { Button } from '@heroui/button';
import { Switch } from '@heroui/switch';
import { Divider } from '@heroui/divider';
import axios from 'axios';
import { useChat } from '@/context/chatContext';
import LoadingProgress from '@/components/LoadingProgress';

const benefits = [
    {
        emoji: '🎯',
        title: 'Zero Guesswork',
        subtitle: 'Specific Courses, No Placeholders',
        description:
            "Every semester filled with actual Truman courses - no more 'Missing Requirements' or 'Electives'. You'll know exactly what to plan.",
    },
    {
        emoji: '⚡',
        title: 'Study What You Love',
        subtitle: 'AI-Powered Course Recommendations',
        description:
            'Our Agent can tailor your course plan to your interests and goals, helping you study what you love, while staying on track for graduation.',
    },
    {
        emoji: '🚀',
        title: 'Plan in Seconds',
        subtitle: 'Hours to minutes',
        description:
            'Get a comprehensive 4-year plan while you finish your coffee. No more spreadsheet headaches or advisor wait times.',
    },
];

const steps = [
    {
        number: '📁',
        title: 'Upload Your Audit',
        description: (
            <p>
                Drag & drop your DegreeWorks PDF{' '}
                <span className="font-bold">
                    (Export as Letter Portrait PDF for best results)
                </span>
            </p>
        ),
    },
    {
        number: '🤖',
        title: 'Choose Your Agent',
        description: (
            <p>
                Long-term planning{' '}
                <span className="italic font-bold">(2-3 minutes)</span> or quick
                Q&A <span className="italic font-bold">(30 seconds)</span>
            </p>
        ),
    },
    {
        number: '🎯',
        title: 'Get Your Plan',
        description: 'Receive a semester-by-semester roadmap to graduation',
    },
];

const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function IndexPage() {
    const navigate = useNavigate();
    const { initializeChat, sessionId } = useChat();
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [prompt, setPrompt] = useState('');
    const [isLongPlanningMode, setIsLongPlanningMode] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [isCheckingSession, setIsCheckingSession] = useState(true);

    // Check if session exists and redirect to chat
    useEffect(() => {
        // Check localStorage directly first (faster than waiting for context)
        const STORAGE_KEY = 'trudegree_chat';
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try {
                const data = JSON.parse(stored);
                if (data.sessionId && data.messages) {
                    // Session exists, redirect to chat
                    navigate('/chat');
                    return;
                }
            } catch (error) {
                console.error('Error checking session:', error);
                // Clear corrupted data
                localStorage.removeItem(STORAGE_KEY);
            }
        }

        // Also check context (in case localStorage was just cleared or context updated)
        if (sessionId) {
            navigate('/chat');
        } else {
            // No session found, show landing page
            setIsCheckingSession(false);
        }
    }, [sessionId, navigate]);

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        setSelectedFile(file || null);
        setError(null);
    };

    const handleSubmit = async () => {
        // Validation
        if (!selectedFile) {
            setError('Please upload a PDF file');
            return;
        }
        if (!prompt.trim()) {
            setError('Please enter a prompt');
            return;
        }

        setIsSubmitting(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('prompt', prompt);
            formData.append(
                'is_long_planning_mode',
                String(isLongPlanningMode)
            );

            const response = await axios.post(
                `${API_BASE_URL}/api/pdf`,
                formData
            );

            // Initialize chat context with session and response
            if (response.data.session_id) {
                initializeChat(response.data.session_id, {
                    ...response.data,
                    userMessage: prompt, // Store the initial prompt
                });

                // Navigate to chat page
                navigate('/chat');
            }
        } catch (error) {
            setError(
                error instanceof Error ? error.message : 'Failed to submit form'
            );
            console.error('Error submitting form:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    // Show loading state while checking session
    if (isCheckingSession) {
        return (
            <DefaultLayout>
                <div className="flex items-center justify-center min-h-[60vh]">
                    <div className="text-center text-default-500">
                        Loading...
                    </div>
                </div>
            </DefaultLayout>
        );
    }

    return (
        <DefaultLayout>
            {/* Hero Section */}
            <section className="flex flex-col items-center justify-center gap-4 py-8 md:pt-3">
                <div className="inline-block max-w-lg text-center justify-center">
                    <span
                        className={`font-black ${title({ color: 'violet', size: 'lg' })}`}
                    >
                        TruDegree&nbsp;
                    </span>
                    <span
                        className={title({
                            fullWidth: true,
                            size: 'sm',
                            className: 'mt-2',
                        })}
                    >
                        Your AI Academic Advisor
                    </span>
                    <div className={subtitle({ class: 'mt-2' })}>
                        Graduate On Time, Stress-Free, Studying What You Love
                    </div>
                </div>
            </section>

            {/* Benefit Cards Section */}
            <section className="flex flex-col items-center justify-center gap-6 py-8 md:py-0 px-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-10 max-w-7xl w-full">
                    {benefits.map((benefit, index) => (
                        <Card
                            key={index}
                            className="p-5"
                            shadow="md"
                            radius="lg"
                            isBlurred
                            isHoverable
                        >
                            <CardHeader className="flex flex-col items-start gap-2 pb-4">
                                <div className="text-3xl mb-2">
                                    {benefit.emoji}
                                </div>
                                <h3 className="text-xl font-bold">
                                    {benefit.title}
                                </h3>
                                <p className="text-sm text-default-600 font-semibold">
                                    {benefit.subtitle}
                                </p>
                            </CardHeader>
                            <CardBody className="pt-0">
                                <p className="text-default-600 text-sm">
                                    {benefit.description}
                                </p>
                            </CardBody>
                        </Card>
                    ))}
                </div>
            </section>

            <Divider className="mt-10" />

            {/* Upload and Chat Section */}
            <section className="grid grid-cols-2  gap-20 py-8 md:py-6 px-4 mb-20 max-w-7xl mx-auto">
                <div className="flex flex-col justify-baseline gap-2">
                    <div className="flex flex-col gap-2 mb-5">
                        <h2 className="text-2xl font-bold">Get Started</h2>
                        <p className="text-sm text-default-600">
                            Upload your DegreeWorks PDF and ask your question
                        </p>
                    </div>
                    <div className="flex flex-col gap-3">
                        <label className="text-sm font-medium text-foreground">
                            PDF File <span className="text-danger">*</span>
                        </label>
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept=".pdf"
                            onChange={handleFileSelect}
                            required
                            className="hidden"
                        />
                        <Button
                            variant="bordered"
                            className="w-full p-6 italic font-bold"
                            onPress={() => fileInputRef.current?.click()}
                            isDisabled={isSubmitting}
                        >
                            {selectedFile
                                ? selectedFile.name
                                : 'Upload DegreeWorks PDF (Letter Portrait PDF for best results)'}
                        </Button>
                        {selectedFile && (
                            <p className="text-xs text-default-500">
                                {selectedFile.name} (
                                {(selectedFile.size / 1024).toFixed(2)} KB)
                            </p>
                        )}
                        <div className="flex items-center justify-between p-3 rounded-lg bg-default-100">
                            <div className="flex flex-col">
                                <span className="text-sm font-semibold">
                                    {isLongPlanningMode
                                        ? 'Long Planning Mode'
                                        : 'Normal Tasks Mode'}
                                </span>
                                <span className="text-xs text-default-600">
                                    {isLongPlanningMode
                                        ? 'Comprehensive 4-year planning, longer wait time (2-3 minutes)'
                                        : 'Quick Q&A and short-term planning, shorter wait time (30 seconds)'}
                                </span>
                            </div>
                            <Switch
                                isSelected={isLongPlanningMode}
                                onValueChange={setIsLongPlanningMode}
                                color="secondary"
                                isDisabled={isSubmitting}
                            />
                        </div>

                        {/* Prompt Textarea */}
                        <div className="flex flex-col gap-2">
                            <label className="text-sm font-medium text-foreground">
                                Prompt <span className="text-danger">*</span>
                            </label>
                            <textarea
                                value={prompt}
                                onChange={(e) => {
                                    setPrompt(e.target.value);
                                    setError(null);
                                }}
                                placeholder="Ask a question or request a plan..."
                                required
                                rows={6}
                                disabled={isSubmitting}
                                className="w-full px-3 py-2 text-sm bg-transparent border border-default-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary focus:border-transparent resize-y min-h-[120px] disabled:opacity-50 disabled:cursor-not-allowed"
                            />
                        </div>

                        {/* Loading Progress */}
                        <LoadingProgress
                            mode="pdf"
                            isLongPlanning={isLongPlanningMode}
                            isVisible={isSubmitting}
                        />

                        {error && (
                            <div className="p-3 rounded-lg bg-danger-50 text-danger text-sm">
                                {error}
                            </div>
                        )}

                        <Button
                            size="lg"
                            color="secondary"
                            onPress={handleSubmit}
                            isDisabled={
                                !selectedFile || !prompt.trim() || isSubmitting
                            }
                            isLoading={isSubmitting}
                            className="w-full"
                            variant="shadow"
                        >
                            {isSubmitting ? 'Processing...' : 'Send'}
                        </Button>
                    </div>
                    {/* AI Mode Toggle */}
                </div>

                <div className="flex flex-col items-center justify-center gap-2">
                    <h2
                        className={title({
                            size: 'md',
                            color: 'yellow',
                            className: 'mb-0 text-center',
                        })}
                    >
                        How It Works
                    </h2>
                    <p className="text-center text-default-600 max-w-2xl">
                        Simple 3-Step Process
                    </p>
                    <Divider className="my-5" />
                    <div className="flex flex-col md:flex-row gap-7 w-full">
                        {steps.map((step, index) => (
                            <div
                                key={index}
                                className="flex flex-col items-center justify-center gap-2"
                            >
                                <div className="flex items-center text-center text-lg font-bold">
                                    {step.number}
                                </div>
                                <h3 className="text-md font-bold">
                                    {step.title}
                                </h3>

                                <p className="text-default-600 text-sm text-center">
                                    {step.description}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>
        </DefaultLayout>
    );
}
