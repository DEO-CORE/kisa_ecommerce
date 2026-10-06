import { useEffect, useRef, type ReactNode } from 'react';
import { X } from 'lucide-react';
import './modal.scss';

interface ModalProps {
    open: boolean;
    onClose: () => void;
    title: string;
    children: ReactNode;
    className?: string;
}

export const Modal = ({ open, onClose, title, children, className = '' }: ModalProps) => {
    const ref = useRef<HTMLDialogElement>(null);

    useEffect(() => {
        const dialog = ref.current;
        if (!open || !dialog) return;
        const overflow = document.body.style.overflow;
        dialog.showModal();
        document.body.style.overflow = 'hidden';
        return () => {
            dialog.close();
            document.body.style.overflow = overflow;
        };
    }, [open]);

    return (
        <dialog
            className={`modal ${className}`}
            ref={ref}
            aria-label={title}
            onCancel={onClose}
            onClick={(event) => { if (event.target === event.currentTarget) onClose(); }}
        >
            <div className="modal__body">
                <button className="modal__close" type="button" onClick={onClose} aria-label="Закрыть">
                    <X className="modal__close-icon" size={24} strokeWidth={1.5} />
                </button>
                {children}
            </div>
        </dialog>
    );
};
