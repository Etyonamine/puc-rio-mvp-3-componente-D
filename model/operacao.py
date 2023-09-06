import datetime
from typing import Union
from sqlalchemy import Column, String, Integer, DateTime,ForeignKey
from model import Base
from sqlalchemy.orm import relationship
class Operacao(Base):
    __tablename__ = 'operacao'
    codigo = Column("id_operacao", Integer, primary_key=True)    
    data_entrada = Column("dt_entrada",DateTime)
    data_saida = Column("dt_saida",DateTime)
    codigo_veiculo = Column("id_veiculo",Integer)
    codigo_tipo_operacao = Column("id_operacao_tip", Integer,\
                             ForeignKey("tipo_operacao.id_operacao_tip"),
                             nullable=False)                             
    observacao = Column("ds_observacao", String(300))    
    data_insercao = Column(DateTime, default= datetime.now())                             
    tipo_operacao = relationship("TipoOperacao", back_populates="operacoes")

    ## criar o vinculo com os modelos do veiculo
    """ modelos = relationship("Modelo", cascade="all,delete",
                                back_populates="marca")  """
    
    def __init__(self, codigo_veiculo: Integer,
                codigo_tipo_operacao: Integer, 
                data_insercao:Union[DateTime, None] = None):
        """
        Cria uma marca de veiculo

        Argumentos:
            sigla: sigla do tipo de operacao E-EVENTUAL / D-DIARIO / M-MENSAL
            codigo do tipo de operacao
            data_insercao quando a operacao foi feito ou inserido
                           à base
        """
        self.data_entrada = data_insercao
        self.codigo_veiculo = codigo_veiculo
        self.codigo_tipo_operacao = codigo_tipo_operacao