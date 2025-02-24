import sys
from Cocoa import (
    NSObject, NSApplication, NSWindow, NSButton, NSMakeRect, NSOpenPanel, NSModalResponseOK,
    NSViewMinXMargin, NSViewMaxXMargin, NSViewMinYMargin, NSViewMaxYMargin
)
from PyObjCTools import AppHelper
import objc


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        # Criação da janela principal (tamanho 4x maior que base: 1600x800)
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            ((200.0, 300.0), (1600.0, 800.0)),
            15,  # Estilo da janela (ajuste conforme necessário)
            2,  # NSBackingStoreBuffered
            False
        )
        self.window.setTitle_("Adaptative Context Code Assistant")
        self.window.makeKeyAndOrderFront_(None)

        # Dimensões do botão
        button_width = 200
        button_height = 40

        # Cálculo para centralizar o botão na janela
        window_width = 1600.0
        window_height = 800.0
        x = (window_width - button_width) / 2
        y = (window_height - button_height) / 2

        # Criação do botão com frame centralizado
        button = NSButton.alloc().initWithFrame_(NSMakeRect(x, y, button_width, button_height))
        button.setTitle_("Selecionar Pasta")
        button.setTarget_(self)
        button.setAction_("selecionarPasta:")
        # Configuração da máscara de redimensionamento para manter o botão centralizado
        button.setAutoresizingMask_(NSViewMinXMargin | NSViewMaxXMargin | NSViewMinYMargin | NSViewMaxYMargin)
        self.window.contentView().addSubview_(button)

    def selecionarPasta_(self, sender):
        panel = NSOpenPanel.openPanel()
        panel.setCanChooseDirectories_(True)
        panel.setCanChooseFiles_(False)
        panel.setAllowsMultipleSelection_(False)

        result = panel.runModal()
        if result == NSModalResponseOK:
            folder_url = panel.URLs()[0]
            folder_path = folder_url.path()
            print(f"Pasta selecionada: {folder_path}")
            # Chama a função placeholder para criação do grafo de conhecimento
            self.criarGrafoConhecimento(folder_path)

    @objc.python_method
    def criarGrafoConhecimento(self, folder_path):
        # Função placeholder para criação do grafo de conhecimento
        print(f"[Placeholder] Criando grafo de conhecimento para a pasta: {folder_path}")


if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
